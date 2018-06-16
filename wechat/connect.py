# -*-coding:utf-8 -*-
import falcon
from falcon import uri
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply

from utils import img_download, img_upload
from face_id import access_api


class Connect(object):

    def on_get(self, req, resp):
        query_string = req.query_string
        query_list = query_string.split('&')
        b = {}
        for i in query_list:
            b[i.split('=')[0]] = i.split('=')[1]

        try:
            check_signature(token='lengxiao', signature=b['signature'], timestamp=b['timestamp'], nonce=b['nonce'])
            resp.body = (b['echostr'])
        except InvalidSignatureException:
            pass
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        xml = req.stream.read()
        msg = parse_message(xml)
        if msg.type == 'text':
            reply = TextReply(content=msg.content, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200
        elif msg.type == 'image':
            name = img_download(msg.image, msg.source)  
            print(name)
            r = access_api('images/' + name)
            if r == 'success':
                media_id = img_upload('image', 'faces/' + name)
                reply = ImageReply(media_id=media_id, message=msg)
            else:
                reply = TextReply(content='人脸检测失败，请上传1M以下人脸清晰的照片', message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200

app = falcon.API()
connect = Connect()
app.add_route('/connect', connect)
