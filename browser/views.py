# coding=utf-8
from django.shortcuts import render_to_response


def index(request):
    from eulexistdb import db

    xmldb = db.ExistDB()

    return render_to_response('browser/index.html')
