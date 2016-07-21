#!/bin/python 
import rbd
import rados
cluster = rados.Rados(conffile='my_ceph.conf')
cluster.connect()

ioctx = cluster.open_ioctx('wwd')
rbd_inst = rbd.RBD()
ioctx = cluster.open_ioctx('wwd')
print "\nWriting object 'hw' with contents 'Hello World!' to pool 'data'."
ioctx.write_full("hw", "Hello World!")

print "\n\nContents of object 'hw'\n------------------------\n"
print ioctx.read("hw")

print "\nRemoving object 'hw'"
ioctx.remove_object("hw")
data = 'tes2'*1000
ioctx.close()
print "=================="
cluster_stats = cluster.get_cluster_stats()
for key, value in cluster_stats.iteritems():
     print key, value
cluster.shutdown()
