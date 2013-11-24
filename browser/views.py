# coding=utf-8
from django.shortcuts import render_to_response


def index(request):
    from eulexistdb.db import ExistDB
    from eulexistdb.query import QuerySet
    from eulxml.xmlmap.teimap import Tei

    qs = QuerySet(using=ExistDB(), xpath='/*:TEI', model=Tei)

    return render_to_response('browser/index.html', {'tei_documents': qs})
