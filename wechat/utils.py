import requests
import json
import threading
import time
import os

token = ''
app_id = 'wxfc6adcdd7593a712'
secret = '429d85da0244792be19e0deb29615128'


def img_download(url, name):
    r = requests.get(url)
    with open('images/{}-{}.jpg'.format(name, time.strftime("%Y_%m_%d%H_%M_%S", time.localtime())), 'wb') as fd:
        fd.write(r.content)
    if os.path.getsize(fd.name) >= 1048576:
        return 'large'
    # print('namename', os.path.basename(fd.name))
    return os.path.basename(fd.name)


def get_access_token(appid, secret):
    '''获取access_token,100分钟刷新一次'''

    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(appid, secret)
    r = requests.get(url)
    parse_json = json.loads(r.text)
    global token
    token = parse_json['access_token']
    global timer
    timer = threading.Timer(6000, get_access_token)
    timer.start()


def img_upload(mediaType, name):
    global token
    url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (token, mediaType)
    files = {'media': open('{}'.format(name), 'rb')}
    r = requests.post(url, files=files)
    parse_json = json.loads(r.text)
    return parse_json['media_id']

get_access_token(app_id, secret)