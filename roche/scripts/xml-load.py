# coding=utf-8

#
# Must be called in roche root dir
#

import collections
import os
import sys

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
        for filename in sorted(filenames):
            with open(os.path.join(dirpath, filename)) as f:
                print "--" + os.path.join(dirpath, filename)
                try:
                    xmldb.load(f, os.path.join('docker', 'texts', dirpath, filename), True)
                except:
                    print "FAILED TO LOAD!!! " + filename

#
# Load resources
#
for (dirpath, dirnames, filenames) in walk('resources'):
    xmldb.createCollection('docker' + '/' + dirpath, True)
    if filenames:
        for filename in filenames:
            with open(dirpath + '/' + filename) as f:
                xmldb.load(f, os.path.join('docker', dirpath, filename), True)

#
# Load TEI into solr
#
si = sunburnt.SolrInterface(SOLR_SERVER_URL + '/')

qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=RocheTEI)

i=0
for q in qs:
    print i

    doc = collections.defaultdict(list)
    for div in q.body.div:
        text = div.text.replace(" ", "").replace("\n", "")
        doc["text"].append(text)

    i = i + 1
    doc['id'] = q.title + '/' + str(q.chapter)
    doc['title'] = q.title
    doc['author'] = q.author

    chapter = q.chapter
    if chapter == None:
        print "WARNING: " + q.title + " has empty chapter"
        chapter = 1
    doc['chapter'] = chapter
    si.add(doc)
    si.commit()
