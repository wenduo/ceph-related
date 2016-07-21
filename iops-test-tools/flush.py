#!/bin/python 
import rbd
import rados
import random, string
import time
import sys   
import multiprocessing
def random_str(randomlength):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

def rados_write(ioctx, key, lenth):
    value = random_str(1)*lenth    
    r=ioctx.write(str(key), value)
    print key,r,len(value)

def flush(value_lenth):
    cluster = rados.Rados(conffile='my_ceph.conf')
    cluster.connect()
    ioctx = cluster.open_ioctx('wwd2')
    for i in range(1,9999):
         rados_write(ioctx,str(i),value_lenth)
    print "flush data to:",value_lenth
    ioctx.close()
    cluster.shutdown()

class FlushProcess(multiprocessing.Process):
    def __init__(self, process_id,data_lenth,start_num,end_num):
        multiprocessing.Process.__init__(self)
        self.process_id = process_id
        self.data_lenth = data_lenth
        self.start_num = start_num
        self.end_num = end_num
    def run(self):
        cluster = rados.Rados(conffile='my_ceph.conf')
        cluster.connect()
        ioctx = cluster.open_ioctx('wwd2')
        for i in range(self.start_num,self.end_num):
            rados_write(ioctx,i,self.data_lenth)
        ioctx.close()
        cluster.shutdown()

if __name__ == "__main__":
     data_lenth = 500000
     process_num = 50
     flushprocs = list()
     for i in range(0,process_num+1):
          print i
          flushprocs.append(FlushProcess(i,data_lenth,2000*i+1000,2000*i+2000))
     for i in flushprocs:
          i.start()
     for i in flushprocs:
          i.join()

