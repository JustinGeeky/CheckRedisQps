#!/usr/bin/python
'''
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
 
   CheckRedisQps.py
 
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
 
The function of this module is to roughly calculate the QPS of Redis.
 
Copyright @Huangyunpeng
 
Date: 2018/9/17
 
  
'''
from os import popen
from time import sleep
import datetime
import sys
import argparse
 
 
def InquireRedis(ip,port,answer):
    reqproccess = popen("redis-cli -h %s -p %s -a %s info | grep total_commands_processed | awk -F ':' '{print $2}'" %(ip,port,answer)).read()
    return int(reqproccess)
 
def QpsCount(ip,port,answer,interval):
    start = InquireRedis(ip,port,answer)
    sleep(interval)
    end = InquireRedis(ip,port,answer)
    if interval == 0:
        return ''
    qps = (end - start) / interval
    return start,end,qps
 
def LoopMonitor(ip,port,answer,interval,cycles):
    for i in range(cycles):
        start,end,qps = QpsCount(ip,port,answer,interval)
        print start,'          |',end,'          |',cycles,'          |',interval,'          |',qps,'          |'
 
def init():
    parser = argparse.ArgumentParser(description="example:[ python CheckRedisQps.py -i 10.10.10.10 -p 6379 -a 1234567 --interval 10.0  -c 10000 ]")
    parser.add_argument('-i','--ip',help='Connect redis by this ip.eg:10.10.10.10')
    parser.add_argument('-p','--port',help='Connect redis by this port.eg:6379')
    parser.add_argument('-a','--answer',help='Connect redis by this answer.eg:1234567')
    parser.add_argument('-in','--interval',help='Set the statistical interval.eg:10.0')
    parser.add_argument('-c','--cycles',help='Set the number of statistical loops.eg:10000')
    argv = parser.parse_args()
    ip = argv.ip
    port = argv.port
    answer = argv.answer
    interval = argv.interval
    cycles = argv.cycles
    return ip,port,answer,float(interval),int(cycles)
 
if __name__ == '__main__':
    IP,PORT,ANSWER,INTERVAL,CYCLES = init()
    print IP,PORT,ANSWER,INTERVAL,CYCLES
    print '\r\n----------------------------------------------------------------------------------------------'
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print 'Hello,welcome to use my tool!','\r\nThe function of this module is to roughly calculate the QPS of Redis.'
    print '----------------------------------------------------------------------------------------------\r\n'
    print 'StartConnectProccess','  ','EndConnectProccess','  ','QueryInterval','  ','Cycles','   ','QPS'
    LoopMonitor(IP,PORT,ANSWER,INTERVAL,CYCLES)