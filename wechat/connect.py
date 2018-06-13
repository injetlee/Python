import falcon
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply


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
            reply = ImageReply(media_id=msg.media_id, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200


app = falcon.API()
connect = Connect()
app.add_route('/connect', connect)

