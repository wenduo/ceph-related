#!/bin/python 
import rbd
import rados
import random, string
import time
import json
import sys   
import threading
import datetime
import multiprocessing
import Queue
def random_str(randomlength):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

def rados_read(ioctx, key, lenth):
    time1 = time.time()
    a = ioctx.read(key,lenth)
    time2 = time.time()
    read_time = time2 - time1
    if a!=0:
        return 0,read_time
    return 1,read_time

def rados_write(ioctx, key, lenth):
    value = random_str(1)*lenth    
    time1 = time.time()
    r=ioctx.write_full(key, value)
    print r
    time2 = time.time()
    write_time = time2-time1
    return r,write_time

def flush(value_lenth):
    cluster = rados.Rados(conffile='my_ceph.conf')
    cluster.connect()
    ioctx = cluster.open_ioctx('wwd2')
    for i in range(1,9999):
         rados_write(ioctx,str(i),value_lenth)
    print "flush data to:",value_lenth
    ioctx.close()
    cluster.shutdown()

class BenchProcess(multiprocessing.Process):
    def __init__(self, process_id, bench_fun, data_lenth, data_num, result_queue):
        multiprocessing.Process.__init__(self)
        self.bench_fun = bench_fun
        self.process_id = process_id
        self.data_lenth = data_lenth
        self.data_num = data_num
        self.result_queue = result_queue
    def run(self):
        cluster = rados.Rados(conffile='my_ceph.conf')
        cluster.connect()
        ioctx = cluster.open_ioctx('wwd2')
        process_latency = 0
        wrong_num = 0 
        for i in range(1,self.data_num+1):
            key =random.randint(1,99999)
            #key =random_str(20)
            result,entity_latency = self.bench_fun(ioctx,str(key),self.data_lenth)
            if result != 0:
                wrong_num = wrong_num +1
            process_latency  = process_latency  + entity_latency 
        ioctx.close()
        cluster.shutdown()
        q.put([wrong_num,process_latency/data_num])
 

if __name__ == "__main__":

    data_num = 120
    #data_lenths = [10000,50000,100000,200000,500000];
    data_lenth = 500100;
    process_nums =[100];
    for v in process_nums:
        process_num = v
	q = multiprocessing.Queue()  
        processes = list()
	for i in range(1,process_num+1):
	    processes.append( BenchProcess(i,rados_read,data_lenth,data_num,q))
	time1 = time.time()
	for i in processes:
	    i.start()
	for i in processes:
	    i.join()
	time2 = time.time()
        run_time = time2 - time1
        latency = 0
	wrong_num = 0
	for i in range(1,process_num+1):
            [process_wrong_num,process_latency] = q.get()
            latency = latency + process_latency
	    wrong_num = wrong_num + process_wrong_num
        latency = latency /process_num
	data_sum = data_num * process_num
	print "======================================="
        print "start",time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time1))
        print "stop",time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time2))
        print "run time:",run_time
        print "data_lenth:",data_lenth
	print "process_num",process_num
	print "data_sum",data_sum
	print "wrong_sum:",wrong_num
        print "wrong_rate:",wrong_num/data_sum
	print "qps:",data_sum/run_time
	print "mean_latency:",latency
	      
