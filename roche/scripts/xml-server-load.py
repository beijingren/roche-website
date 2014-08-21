# coding=utf-8

#
# Must be called in roche root dir
#

import os


from os import walk
from eulexistdb.db import ExistDB

#
# Timeout higher?
#

#
# http://username:password@54.220.97.75:8080/exist
#
xmldb = ExistDB('http://54.220.97.75:8080/exist')

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
