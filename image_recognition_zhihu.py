# -*- coding:UTF-8 -*-

import  requests , time ,random
import  hmac ,json ,base64
from bs4 import BeautifulSoup
from hashlib import sha1
import TencentYoutuyun
from PIL import Image
import uuid


    
def recognition_captcha(data):
    ''' 识别验证码 '''

    file_id = str(uuid.uuid1())
    filename = 'captcha_'+ file_id +'.gif'
    filename_png =  'captcha_'+ file_id +'.png'

    if(data is None):
        return 
    data = base64.b64decode(data.encode('utf-8'))
    with open( filename ,'wb') as fb:
        fb.write( data )    
    
    appid = 'appid' # 接入优图服务，注册账号获取 
    secret_id = 'secret_id'  
    secret_key = 'secret_key'  
    userid= 'userid' 
    end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT   

    youtu = TencentYoutuyun.YouTu(appid, secret_id, secret_key, userid, end_point) # 初始化

    # 拿到的是gif格式，而优图只支持 JPG PNG BMP 其中之一，这时我们需要 pip install Pillow 来转换格式
    im = Image.open( filename)
    im.save( filename_png ,"png")
    im.close()
    
    result = youtu.generalocr( filename_png , data_type = 0 , seq = '')  #  0代表本地路径，1代表url

    return result


def get_captcha(sessiona,headers):
    ''' 获取验证码 '''
    
    need_cap = False

    while( need_cap is not True):
        try:
            sessiona.get('https://www.zhihu.com/signin',headers=headers)  # 拿cookie:_xsrf
            resp2 = sessiona.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=cn',headers=headers)  # 拿cookie:capsion_ticket 
            need_cap = json.loads(resp2.text)["show_captcha"]  # {"show_captcha":false} 表示不用验证码
            time.sleep( 0.5 + random.randint(1,9)/10 )
        except Exception:
            continue

    try:
        resp3 = sessiona.put('https://www.zhihu.com/api/v3/oauth/captcha?lang=cn',headers=headers) # 拿到验证码数据，注意是put
        img_data = json.loads(resp3.text)["img_base64"]
    except Exception:
        return     
    

    return img_data

def create_point( point_data, confidence ):
    ''' 获得点阵 '''

    # 实际操作下，套路不深，x间隔25，y相同，共7个点 ，先模拟意思一下
    points = {1:[ 20.5,25.1875],2:[ 45.5,25.1875],3:[ 70.5,25.1875],4:[ 95.5,25.1875],5:[120.5,25.1875],6:[145.5,25.1875],7:[170.5,25.1875]}
    wi = 0
    input_points = []
    
    for word in ( point_data['items'][0]['words'] ):
        wi = wi+1
        if( word['confidence'] < confidence ):
            try:
                input_points.append(points[wi]) # 倒置的中文，优图识别不出来，置信度会低于0.5
            except KeyError:
                continue
        
    if( len(input_points) > 2 or len(input_points) == 0 ):
        return []  # 7个字中只有2个倒置中文的成功率高
    
    result = {}
    result['img_size']=[200,44]
    result['input_points']=input_points
    result = json.dumps(result)
    print(result)
    return result

def bolting(k_low,k_hi,k3_confidence):
    ''' 筛选把握大的进行验证 '''

    start = time.time()
    
    is_success = False
    while(is_success is not True):
    
        points_len = 1
        angle = -20
        img_ko = []

        while(points_len != 21  or  angle < k_low  or angle > k_hi ):  
            img_data = get_captcha(sessiona,headers)
            img_ko = recognition_captcha(img_data)
     
            ## json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False
            # img_ko_json = json.dumps(img_ko , indent =2 ,ensure_ascii=False ) 
            # img_ko_json = img_ko_json.encode('raw_unicode_escape') ## 因为python3的原因，也因为优图自身的原因，此处要特殊处理
        
            # with open( "json.txt" ,'wb') as fb:
            #     fb.write( img_ko_json )  
    
            try:
                points_len = len(img_ko['items'][0]['itemstring'])
                angle = img_ko['angle']
            except Exception:
                points_len = 1
                angle = -20
                continue

        # print(img_ko_json.decode('utf8')) ## stdout用的是utf8，需转码才能正常显示
        # print('-'*50)
        
        input_text = create_point( img_ko ,k3_confidence )
        if(type(input_text) == type([])):
            continue
        
        data = {
            "input_text":input_text   
            }

        # 提交过快会被拒绝，{"code":120005,"name":"ERR_VERIFY_CAPTCHA_TOO_QUICK"} ，假装思考5秒钟
        time.sleep( 4 + random.randint(1,9)/10 )
        try:    
            resp5 = sessiona.post('https://www.zhihu.com/api/v3/oauth/captcha?lang=cn',data,headers=headers)
        except Exception:
            continue
        
        print("angle: "+ str(angle) )
        print(BeautifulSoup(resp5.content ,'html.parser')) # 如果验证成功，会回应{"success":true}，开心
        print('-'*50)
        try:
            is_success = json.loads(resp5.text)["success"]
        except KeyError:
            continue

    end = time.time()

    return end-start


if __name__ == "__main__":
    
    sessiona = requests.Session()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0','authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'}

    k3_confidence = 0.71
    
    '''
    # 可视化数据会被保存在云端供浏览
    # https://plot.ly/~weldon2010/4
    # 纯属学习，并未看出"角度"范围扩大对图像识别的影响，大部分时候60s内能搞定，说明优图还是很强悍的，识别速度也非常快
    '''
    runtime_list_x = []
    runtime_list_y = []
    nn = range(1,11) # 愿意的话搞多线程，1百万次更有意思
    
    # 成功尝试100次，形成2维数据以热力图的方式展示
    for y in nn :
        for x in  nn :
            runtime_list_x.append( bolting(-3,3,k3_confidence) )
            print( "y: " + str(runtime_list_y) )
            print( "x: " + str(runtime_list_x) )
        runtime_list_y.append(runtime_list_x.copy())
        runtime_list_x = []

    print ("-"*30)    
    print( runtime_list_y )
    print ("-"*30)

    # pip install plotly 数据可视化
    import plotly
    import plotly.graph_objs as go
    plotly.tools.set_credentials_file(username='username', api_key='username') # 设置账号，去官网注册
    trace = go.Heatmap(z = runtime_list_y , x = [n for n in nn ] ,y =[n for n in nn ])
    data=[trace]
    plotly.plotly.plot(data, filename='weldon-time2-heatmap')    
   
    # 尝试后发现一个特点，基本都是1~2个倒置中文，这样我们可以借此提速
    # 角度范围放大，仅当识别出倒置中文为1~2个时才提交验证否则放弃继续寻找

### chcp 65001 (win下改变cmd字符集)
### python  c:\python34\image_recognition_zhihu.py






