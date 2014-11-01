import os

from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from eulexistdb.db import ExistDB
from eulexistdb.query import QuerySet

from browser.models import RocheTEI


@cache_page(60 * 60)
def index(request):
    # XML and SPARQL numbers

    # Count texts and authors
    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=RocheTEI)
    qs = qs.filter(chapter='1')
    qs = qs.only('title', 'title_en', 'author')
    # TODO: order by title
    qs = qs.order_by('title_en')

    number_texts = qs.count()
    number_authors = qs.distinct().count()

    wiki_pages = []
    for page in sorted(os.listdir("/docker/dublin-store/sinology/mainSpace")):
        wiki_pages.append([page.replace(" ", "%20"), page])

    data = {'number_texts': number_texts, 'number_authors': number_authors,
            'tei_documents': qs, "wiki_pages": wiki_pages, }

    return render(request, 'roche/index.html', data)
