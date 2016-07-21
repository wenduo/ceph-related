#!/bin/sh
for i in $( seq 1 3 )
do
    #./qps_latency.py &> "log"$i
    ./qps_latency.py &>>log
done 
