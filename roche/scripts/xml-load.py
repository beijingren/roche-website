# coding=utf-8

#
# Must be called in roche root dir
#

import sys
import os

sys.path.append('.')
import roche.settings

from os import walk
from eulexistdb.db import ExistDB
from roche.settings import EXISTDB_SERVER_URL

#
# Timeout higher?
#
xmldb = ExistDB(timeout=30)

xmldb.createCollection('docker', True)

os.chdir('../dublin-store')

for (dirpath, dirnames, filenames) in walk('浙江大學圖書館'):
    xmldb.createCollection('docker' + '/' + dirpath, True)
    if filenames:
        for filename in filenames:
            with open(dirpath + '/' + filename) as f:
                xmldb.load(f, 'docker' + '/' + dirpath + '/' + filename, True)
