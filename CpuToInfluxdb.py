import psutil
import os
from influxdb import InfluxDBClient
import time,math,random


#获取当前运行的pid
p1=psutil.Process(os.getpid()) 


from influxdb import InfluxDBClient
import time,math,random
while True:
    a = psutil.virtual_memory().percent  #内存占用率

    b = psutil.cpu_percent(interval=1.0) #cpu占用率

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
    client.create_database('xxyyxx',if_not_exists=False)
    client.write_points(json_body)
    #result = client.query('select value from cpu_load_short;')
    #print("Result: {0}".format(result))
    time.sleep(2)