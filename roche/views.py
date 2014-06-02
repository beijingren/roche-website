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
    qs = qs.only('author').filter(chapter='1')
    number_texts = qs.count()
    number_authors = qs.distinct().count()

    data = {'number_texts': number_texts, 'number_authors': number_authors}
    return render(request, 'roche/index.html', data)
