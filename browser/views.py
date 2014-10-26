# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from eulexistdb.db import ExistDB
from eulexistdb.query import QuerySet
from eulxml.xmlmap.teimap import Tei

from browser.models import RocheTEI
from common.utils import XSL_TRANSFORM_1
from common.utils import XSL_TRANSFORM_2


def index(request):
    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=RocheTEI)

    # Make titles unique (maybe there is a better method?)
    qs = qs.filter(chapter='1')
    qs = qs.only('title', 'title_en', 'author')

    return render_to_response('browser/index.html', {'tei_documents': qs}, context_instance=RequestContext(request))


def index_author(request, author, startswith):
    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=Tei)

    if startswith:
        # filter by authors starting with letter
        qs = qs.filter(author__startswith=author)
    else:
        qs = qs.filter(author=author)

    return render_to_response('browser/index.html', {'tei_documents': qs}, context_instance=RequestContext(request))

def index_title(request, letter):
    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=Tei)

    # filter by titles starting with letter
    qs = qs.filter(title__startswith=letter)

    return render_to_response('browser/index.html', {'tei_documents': qs},
                              context_instance=RequestContext(request))

def text_view(request, title):
    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=RocheTEI)

    # filter by title
    qs = qs.filter(title=title).order_by('chapter')

    max_juan = qs.count()

    result = ""
    for q in qs:
        result = result + q.body.xsl_transform(xsl=XSL_TRANSFORM_1).serialize()

    text_title = qs[0].title

    data = {'tei_documents': qs, 'tei_transform': result,
            'text_title': text_title, 'max_juan': max_juan, }

    return render_to_response('browser/text_view.html', data,
                              context_instance=RequestContext(request))

def text_view_juan(request, title, juan):
    """
    Return a single chapter from a title.
    """

    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=RocheTEI)

    # filter by title
    qs = qs.filter(title=title)

    max_juan = qs.count()

    qs = qs.filter(chapter=juan)
    result = qs[0].body.xsl_transform(xsl=XSL_TRANSFORM_1).serialize()
    text_title = qs[0].title

    data = {'tei_documents': qs, 'tei_transform': result,
            'text_title': text_title, 'max_juan': max_juan, }

    return render_to_response('browser/text_view.html', data,
                              context_instance=RequestContext(request))
