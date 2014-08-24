# coding=utf-8

import tempfile
import os
import subprocess

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import TextAnnotationForm

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
#BERTIE_JAR = "/home/david/SKQS/bertie-uima/target/bertie-uima-0.0.1-SNAPSHOT.jar"

TEI_HEADER = """<?xml version="1.0" encoding="UTF-8" ?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
<teiHeader>
<fileDesc>
<titleStmt>
<title xml:lang="zh">欽定四庫全書總目提要</title>
<title xml:lang="en">Annotated Catalog of the Complete Imperial Library</title>
<author>
<name>
<choice>
<sic>紀昀</sic>
</choice>
</name>
</author>
</titleStmt>

<publicationStmt>
<p>This document is published under a CC Attribution-Share Alike License</p>
</publicationStmt>

<sourceDesc>
<p>XXX</p>
</sourceDesc>
</fileDesc>
</teiHeader>

<text>
<body>

<div type="chapter" n="1">

<div>
<p>
"""

TEI_FOOTER = """</p>
</div>

</div> <!-- Chapter -->

</body>
</text>
</TEI>
"""


def index(request):
    if request.method == 'POST':
        form = TextAnnotationForm(request.POST)
        if form.is_valid():

            text = form.cleaned_data['text']
            f = tempfile.NamedTemporaryFile(delete=False)
            f.write(text.encode('utf-8'))
            f.close()

            error_msg = ''
            # Call UIMA analysis engine
            result = subprocess.call(["/usr/bin/java", "-jar", BERTIE_JAR, f.name])
            if result == -1:
                error_msg = "UIMA error"

            # Read result back in
            f2 = open(f.name, 'r')
            result = f2.read()

            # XSLT transform result
            from eulxml import xmlmap
            from common.utils import XSL_TRANSFORM_1
            from browser.models import RocheTEI

            result = TEI_HEADER + result + TEI_FOOTER
            q = xmlmap.load_xmlobject_from_string(result, xmlclass=RocheTEI)
            result = q.body.xsl_transform(xsl=XSL_TRANSFORM_1).serialize()

            os.unlink(f.name)

            data = {'tei_document': result}
            return render_to_response('annotate/show_result.html', data, context_instance=RequestContext(request))
    else:
        form = TextAnnotationForm(initial={'text': INITIAL_TEXT})

    data = {'form': form }
    return render_to_response('annotate/index.html', data, context_instance=RequestContext(request))
