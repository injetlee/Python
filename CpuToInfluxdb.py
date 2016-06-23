import psutil
import os
from influxdb import InfluxDBClient
import time,math,random


#获取当前运行的pid
p1=psutil.Process(os.getpid()) 

#打印本机的内存信息
#print ('直接打印内存占用： '+(str)(psutil.virtual_memory))

#打印内存的占用率






from influxdb import InfluxDBClient
import time,math,random
while True:
    # for i in range(360):
  
    #     sin = round(random.random()*1000,2)
    #     print (sin)
    a = psutil.virtual_memory().percent

#本机cpu的总占用率
    b = psutil.cpu_percent(interval=1.0)

    json_body = [
        {
            "measurement": "cpu_load_short",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            #"time": "2009-11-10T23:00:00Z",
            "fields": {
                "cpu": b,
                "mem": a
            }
        }
    ]
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'xxyyxx')
    print('aaaaaa')
    #client.create_database('xxyyxx',if_not_exists=False)
    print('bbbbb')
    client.write_points(json_body)
    #result = client.query('select value from cpu_load_short;')
    #print("Result: {0}".format(result))
    time.sleep(2)