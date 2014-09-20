# coding=utf-8

import json
import os
import subprocess
import tempfile
import uuid

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.cache import get_cache_key

from pika import BasicProperties
from pika import BlockingConnection
from pika import ConnectionParameters

from eulxml import xmlmap
from eulexistdb.db import ExistDB


from roche.settings import RABBITMQ_SERVER
from common.utils import XSL_TRANSFORM_1
from browser.models import RocheTEI
from .forms import TextAnnotationForm
from .models import TextAnnotation

#
# Sample test for analysis
#
INITIAL_TEXT = u"""歐陽修，字永叔，廬陵人。四歲而孤，母鄭，守節自誓，親誨之學，家貧，至以荻畫地學書。幼敏悟過人，讀書輒成誦。及冠，嶷然有聲。

宋興且百年，而文章體裁，猶仍五季余習。鎪刻駢偶，淟涊弗振，士因陋守舊，論卑氣弱。蘇舜元、舜欽、柳開、穆修輩，咸有意作而張之，而力不足。修游隨，得唐韓愈遺稿於廢書簏中，讀而心慕焉。苦志探賾，至忘寢食，必欲並轡絕馳而追與之並。
"""

#
# UIMA standalone analysis engine pipeline
#
BERTIE_JAR = "/docker/bertie-uima/target/bertie-uima-0.0.1-SNAPSHOT.jar"

def index(request):
    """
    Show form to annotate a text by UIMA.
    """

    if request.method == 'POST':
        form = TextAnnotationForm(request.POST)
        if form.is_valid():

            text = form.cleaned_data['text']
            f = tempfile.NamedTemporaryFile(delete=False)
            f.write(text.encode('utf-8'))
            f.close()

            error_msg = ''
            # Call UIMA analysis engine
            result = subprocess.call(["/usr/bin/java", "-Dfile.encoding=UTF-8", "-jar", BERTIE_JAR,
                                      "--plain", "--file", f.name])
            if result == -1:
                error_msg = "UIMA error"

            # Read result back in
            f2 = open(f.name, 'r')
            result = f2.read().decode('utf-8')

            textAnnotation = TextAnnotation()
            textAnnotation.text = result
            textAnnotation.text_type = "prosa"
            textAnnotation.save()

            os.unlink(f.name)

            return HttpResponseRedirect(reverse(
                                        'annotate.views.show_annotated',
                                        args=(textAnnotation.id,)))
    else:
        form = TextAnnotationForm(initial={'text': INITIAL_TEXT})

    data = {'form': form }
    return render_to_response('annotate/index.html', data, context_instance=RequestContext(request))

def show_annotated(request, uima_id):
    """
    Show previously annotated UIMA result.
    """

    try:
        uima = TextAnnotation.objects.get(pk=int(uima_id))
        result = uima.text
    except:
        result = ''

    # TODO: catch XMLSyntaxError
    # XSLT transform result
    q = xmlmap.load_xmlobject_from_string(result.encode("utf-8"), xmlclass=RocheTEI)
    result = q.body.xsl_transform(xsl=XSL_TRANSFORM_1).serialize()

    data = {'tei_documents': [q], 'tei_transform': result}
    return render_to_response('browser/text_view.html', data)

def annotate(request, function, lemma):
    from .models import Annotation

    print "POST", function, lemma

    annotation = Annotation()
    annotation.tei_tag = function
    annotation.lemma = lemma
    annotation.ip = request.META['REMOTE_ADDR']
    annotation.save()

    return HttpResponse("OK")

def annotate_text(request, text, function, lemma):
    """
    Annotate a single text. Run UIMA through a remote procedure call.
    """
    from .models import Annotation

    #
    # RPC
    #
    uima_response = {}
    uima_response['response'] = None
    uima_corr_id = str(uuid.uuid4())
    uima_body = json.dumps({'text': text, 'function': function, 'lemma': lemma})

    def uima_on_response(channel, method, props, body):
        if uima_corr_id == props.correlation_id:
            uima_response['response'] = body

    uima_connection = BlockingConnection(ConnectionParameters(host=RABBITMQ_SERVER))
    uima_channel = uima_connection.channel()
    uima_result = uima_channel.queue_declare(exclusive=True)
    uima_callback_queue = uima_result.method.queue
    uima_channel.basic_consume(uima_on_response, no_ack=True, queue=uima_callback_queue)
    uima_channel.basic_publish(exchange='',
                               routing_key='uima_worker',
                               properties=BasicProperties(reply_to=uima_callback_queue,
                                                          content_type='application/json',
                                                          correlation_id = uima_corr_id,),
                               body=uima_body)

    while uima_response['response'] is None:
        uima_connection.process_data_events()

    #
    # Reload TEI files into existdb
    #
    os.chdir('../dublin-store')
    xmldb = ExistDB(timeout=60)
    for (dirpath, dirnames, filenames) in os.walk(u'浙江大學圖書館'):
        if dirpath.endswith(unicode(text)):
            xmldb.createCollection('docker/texts' + '/' + dirpath, True)
            if filenames:
                for filename in filenames:
                    with open(dirpath + '/' + filename) as f:
                        print "--" + dirpath + '/' + filename
                        xmldb.load(f, 'docker/texts' + '/' + dirpath + '/' + filename, True)

    # Invalidate page?
    # TODO

    annotation = Annotation()
    annotation.tei_tag = function
    annotation.lemma = lemma
    annotation.ip = request.META['REMOTE_ADDR']
    annotation.save()

    return HttpResponse("OK")
