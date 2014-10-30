# coding=utf-8

#
# Must be called in roche root dir
#

import sys
import os


DJANGO_SETTINGS_MODULE="roche.settings"

sys.path.append('.')
sys.path.append('..')

import roche.settings

from os import walk
from eulexistdb.db import ExistDB
from roche.settings import EXISTDB_SERVER_URL
from roche.settings import SOLR_SERVER_URL

import sunburnt
import libxslt
import libxml2

from browser.models import RocheTEI
from eulexistdb.query import QuerySet

#
# Timeout higher?
#
xmldb = ExistDB(timeout=60)

xmldb.createCollection('docker', True)
xmldb.createCollection('docker/texts', True)

os.chdir('../dublin-store')

for (dirpath, dirnames, filenames) in walk('浙江大學圖書館'):
    xmldb.createCollection('docker/texts' + '/' + dirpath, True)
    if filenames:
        for filename in filenames:
            with open(dirpath + '/' + filename) as f:
                print "--" + dirpath + '/' + filename
                xmldb.load(f, 'docker/texts' + '/' + dirpath + '/' + filename, True)

#
# Load resources
#
for (dirpath, dirnames, filenames) in walk('resources'):
    xmldb.createCollection('docker' + '/' + dirpath, True)
    if filenames:
        for filename in filenames:
            with open(dirpath + '/' + filename) as f:
                xmldb.load(f, 'docker' + '/' + dirpath + '/' + filename, True)

#
# Load TEI into solr
#
si = sunburnt.SolrInterface(SOLR_SERVER_URL + '/')

qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=RocheTEI)

i=0
for q in qs:
    print i, q.title,

    text = ""
    for div in q.body.div:
        text = text + div.text

    text.replace(" ", "")

    i = i + 1
    document = {"id": i, "text": text, "title": q.title, "author": q.author}
    si.add(document)
    si.commit()
