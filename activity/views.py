from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from eulexistdb.db import ExistDB
from eulexistdb.query import QuerySet

from eulxml import xmlmap

from browser.models import RocheTEI

from annotate.models import TextAnnotation
from annotate.models import Annotation
from common.utils import XSL_TRANSFORM_1


def index(request):

    qs = TextAnnotation.objects.all()

    uima_latest = []
    for uima in qs[:10]:
        q = xmlmap.load_xmlobject_from_string(uima.text.encode("utf-8"), xmlclass=RocheTEI)
        result = q.body.xsl_transform(xsl=XSL_TRANSFORM_1).serialize()
        # Remove div and p
        uima_latest.append([uima, result])


    qs = Annotation.objects.all()

    annotation_latest = qs[:100]

    data = {'uima_latest': uima_latest, 'annotation_latest': annotation_latest, }
    return render(request, 'activity/index.html', data)
