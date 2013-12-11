# encoding: utf-8
from django.shortcuts import render_to_response

from eulexistdb.db import ExistDB
from eulexistdb.query import QuerySet

from browser.models import RocheTEI


def index(request):
    xmldb = ExistDB()
    qs = QuerySet(using=xmldb, xpath='/tei:TEI', collection='docker/texts/',
                  model=RocheTEI, fulltext_options={'default-operator': 'and'})    
    qs = qs.filter(body__fulltext_terms='至')

    return render_to_response('search/index.html', {'tei_documents': qs})
