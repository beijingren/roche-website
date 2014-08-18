from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from eulexistdb.db import ExistDB
from eulexistdb.query import QuerySet

from browser.models import RocheTEI


cache_page(60 * 60)
def index(request):
    # XML and SPARQL numbers
    # Page should be cached

    # Count texts and authors
    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=RocheTEI)
    qs = qs.filter(chapter='1')
    qs = qs.only('title', 'title_en', 'author')

    number_texts = qs.count()
    number_authors = qs.distinct().count()

    data = {'number_texts': number_texts, 'number_authors': number_authors, 'tei_documents': qs}
    return render(request, 'roche/index.html', data)
