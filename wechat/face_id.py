# -*-coding:utf-8 -*-
import time
import random
import base64
import hashlib
import requests
from urllib.parse import urlencode
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os


# 一.计算接口鉴权，构造请求参数

def random_str():
    '''得到随机字符串nonce_str'''
    str = 'abcdefghijklmnopqrstuvwxyz'
    r = ''
    for i in range(15):
        index = random.randint(0,25)
        r += str[index]
    return r


def image(name):
    with open(name, 'rb') as f:
        content = f.read()
    return base64.b64encode(content)


def get_params(img):
    '''组织接口请求的参数形式，并且计算sign接口鉴权信息，
    最终返回接口请求所需要的参数字典'''
    params = {
        'app_id': '1106860829',
        'time_stamp': str(int(time.time())),
        'nonce_str': random_str(),
        'image': img,
        'mode': '0'

    }

    sort_dict = sorted(params.items(), key=lambda item: item[0], reverse=False)  # 排序
    sort_dict.append(('app_key', 'P8Gt8nxi6k8vLKbS'))  # 添加app_key
    rawtext = urlencode(sort_dict).encode()  # URL编码
    sha = hashlib.md5()
    sha.update(rawtext)
    md5text = sha.hexdigest().upper()  # 计算出sign，接口鉴权
    params['sign'] = md5text  # 添加到请求参数列表中
    return params

# 二.请求接口URL


def access_api(img):
    frame = cv2.imread(img)
    nparry_encode = cv2.imencode('.jpg', frame)[1]
    data_encode = np.array(nparry_encode)
    img_encode = base64.b64encode(data_encode)  # 图片转为base64编码格式
    url = 'https://api.ai.qq.com/fcgi-bin/face/face_detectface' 
    res = requests.post(url, get_params(img_encode)).json()  # 请求URL,得到json信息
    # 把信息显示到图片上
    if res['ret'] == 0:  # 0代表请求成功
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # 把opencv格式转换为PIL格式，方便写汉字
        draw = ImageDraw.Draw(pil_img)
        for obj in res['data']['face_list']:
            img_width = res['data']['image_width']  # 图像宽度
            img_height = res['data']['image_height']  # 图像高度
            # print(obj)
            x = obj['x']  # 人脸框左上角x坐标
            y = obj['y']  # 人脸框左上角y坐标
            w = obj['width']  # 人脸框宽度
            h = obj['height']  # 人脸框高度
            # 根据返回的值，自定义一下显示的文字内容
            if obj['glass'] == 1:  # 眼镜
                glass = '有'
            else:
                glass = '无'
            if obj['gender'] >= 70:  # 性别值从0-100表示从女性到男性
                gender = '男'
            elif 50 <= obj['gender'] < 70:
                gender = "娘"
            elif obj['gender'] < 30:
                gender = '女'
            else:
                gender = '女汉子'
            if 90 < obj['expression'] <= 100:  # 表情从0-100，表示笑的程度
                expression = '一笑倾城'
            elif 80 < obj['expression'] <= 90:
                expression = '心花怒放'
            elif 70 < obj['expression'] <= 80:
                expression = '兴高采烈'
            elif 60 < obj['expression'] <= 70:
                expression = '眉开眼笑'
            elif 50 < obj['expression'] <= 60:
                expression = '喜上眉梢'
            elif 40 < obj['expression'] <= 50:
                expression = '喜气洋洋'
            elif 30 < obj['expression'] <= 40:
                expression = '笑逐颜开'
            elif 20 < obj['expression'] <= 30:
                expression = '似笑非笑'
            elif 10 < obj['expression'] <= 20:
                expression = '半嗔半喜'
            elif 0 <= obj['expression'] <= 10:
                expression = '黯然伤神'
            delt = h // 5  # 确定文字垂直距离
            # 写入图片
            if len(res['data']['face_list']) > 1:  # 检测到多个人脸，就把信息写入人脸框内
                font = ImageFont.truetype('yahei.ttf', w // 8, encoding='utf-8')  # 提前把字体文件下载好
                draw.text((x + 10, y + 10), '性别 :' + gender, (76, 176, 80), font=font)
                draw.text((x + 10, y + 10 + delt * 1), '年龄 :' + str(obj['age']), (76, 176, 80), font=font)
                draw.text((x + 10, y + 10 + delt * 2), '表情 :' + expression, (76, 176, 80), font=font)
                draw.text((x + 10, y + 10 + delt * 3), '魅力 :' + str(obj['beauty']), (76, 176, 80), font=font)
                draw.text((x + 10, y + 10 + delt * 4), '眼镜 :' + glass, (76, 176, 80), font=font)
            elif img_width - x - w < 170:  # 避免图片太窄，导致文字显示不完全
                font = ImageFont.truetype('yahei.ttf', w // 8, encoding='utf-8')
                draw.text((x + 10, y + 10), '性别 :' + gender, (76, 176, 80), font=font)
                draw.text((x + 10, y + 10 + delt * 1), '年龄 :' + str(obj['age']), (76, 176, 80), font=font)
                draw.text((x + 10, y + 10 + delt * 2), '表情 :' + expression, (76, 176, 80), font=font)
                draw.text((x + 10, y + 10 + delt * 3), '魅力 :' + str(obj['beauty']), (76, 176, 80), font=font)
                draw.text((x + 10, y + 10 + delt * 4), '眼镜 :' + glass, (76, 176, 80), font=font)
            else:
                font = ImageFont.truetype('yahei.ttf', 20, encoding='utf-8')
                draw.text((x + w + 10, y + 10), '性别 :' + gender, (76, 176, 80), font=font)
                draw.text((x + w + 10, y + 10 + delt * 1), '年龄 :' + str(obj['age']), (76, 176, 80), font=font)
                draw.text((x + w + 10, y + 10 + delt * 2), '表情 :' + expression, (76, 176, 80), font=font)
                draw.text((x + w + 10, y + 10 + delt * 3), '魅力 :' + str(obj['beauty']), (76, 176, 80), font=font)
                draw.text((x + w + 10, y + 10 + delt * 4), '眼镜 :' + glass, (76, 176, 80), font=font)

            draw.rectangle((x, y, x + w, y + h), outline="#4CB050")  # 画出人脸方框
            cv2img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)  # 把 pil 格式转换为 cv
            cv2.imwrite('faces/{}'.format(os.path.basename(img)), cv2img)  # 保存图片到 face 文件夹下
        return 'success'
    else:
        return 'fail'