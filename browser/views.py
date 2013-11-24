# coding=utf-8
from django.shortcuts import render_to_response

from eulexistdb.db import ExistDB
from eulexistdb.query import QuerySet
from eulxml.xmlmap.teimap import Tei


def index(request):
    qs = QuerySet(using=ExistDB(), xpath='/*:TEI', model=Tei)

    return render_to_response('browser/index.html', {'tei_documents': qs})

def index_author(request, letter):
    qs = QuerySet(using=ExistDB(), xpath='/*:TEI', model=Tei)

    # filter by authors starting with letter
    gs = gs.filter(author__startswith=letter)

    return render_to_response('browser/index.html', {'tei_documents': qs})

def index_title(request, letter):
    qs = QuerySet(using=ExistDB(), xpath='/*:TEI', model=Tei)

    # filter by titles starting with letter
    qs = qs.filter(title__startswith=letter)

    return render_to_response('browser/index.html', {'tei_documents': qs})
