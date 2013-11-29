# coding=utf-8

#
# Must be called in roche root dir
#

import sys
sys.path.append('.')
import roche.settings

from eulexistdb.db import ExistDB
from roche.settings import EXISTDB_SERVER_URL

#
# Timeout higher?
#
xmldb = ExistDB(timeout=30)

xmldb.createCollection('docker', True)
xmldb.createCollection(u'docker/浙江大學圖書館', True)

with open('../dublin-store/db/test_001.xml') as f:
    xmldb.load(f, '/docker/001.xml', True)

