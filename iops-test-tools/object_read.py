#!/bin/python 
import rbd
import rados
import random, string
import time

import json
import sys   

def random_str(randomlength):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

cluster = rados.Rados(conffile='my_ceph.conf')
cluster.connect()
ioctx = cluster.open_ioctx('wwd2')
key =  "Dfgdahfsal;kefjlk;d;sGVL;KADJ"
ioctx.write_full(key, "haha")
ioctx.write(str(key), "11")
ioctx.write(str(key), "22")
r = ioctx.read(str(key))
print r
ioctx.close()
cluster.shutdown()
