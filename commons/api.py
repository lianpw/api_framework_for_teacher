import base64
import hashlib
import os
import random
import time

import rsa
import yaml
from flask import Flask, request

#初始化一个实例
from commons.request_util import RequestUtil
from hotloads.test import Test

app = Flask(__name__)

#MD5加密
def md5_jm(args):
    return hashlib.md5(str(args).encode('utf-8')).hexdigest()

#Base64加密
def base64_jm(args):
    return base64.b64encode(str(args).encode("utf-8")).decode(encoding ="utf-8")

############################  RSA双钥加密  ############################
#生成公钥和私钥写入到指定的pem文件
def create_key():
    #根据秘钥长度生成公钥和私钥
    (public_key,private_key) = rsa.newkeys(1024)
    #保存公钥
    with open("./public.pem","w+") as f:
        f.write(public_key.save_pkcs1().decode())
    # 保存私钥
    with open("./private.pem","w+") as f:
        f.write(private_key.save_pkcs1().decode())

#通过公钥加密
def rsa_jiami(args):
    #导入公钥
    with open("public.pem") as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
    #加密
    byte_str = rsa.encrypt(str(args).encode("utf-8"),pubkey)
    #把二进制转化成字符串格式
    miwen = base64.b64encode(byte_str).decode("utf-8")
    return miwen

#通过私钥解密
def rsa_jiemi(args):
    # 导入私钥
    with open("private.pem") as f:
        prikey = rsa.PrivateKey.load_pkcs1(f.read().encode())
    #把字符串转换成二进制格式
    byte_str = base64.b64decode(str(args).encode("utf-8"))
    #解密
    mingwen = rsa.decrypt(byte_str,prikey).decode()
    return mingwen

############################  Sign签名  ############################
# def signs(self,yaml_path):
#     last_url = ""
#     last_data = {}
#     with open(os.getcwd()+yaml_path,encoding='utf-8') as f:
#         yaml_value = yaml.load(f,Loader=yaml.FullLoader)
#         for caseinfo in yaml_value:
#             caseinfo_keys = caseinfo.keys()
#             # 判断一级关键字是否包括有:name,request,validate
#             if "request" in caseinfo_keys:
#                 # 判断url
#                 if "url" in caseinfo['request'].keys():
#                     last_url=caseinfo['request']['url']
#                 # 判断参数
#                 req = caseinfo['request']
#                 for key,value in req.items():
#                     if key in ['params','data','json']:
#                         for p_key,p_value in req[key].items():
#                             last_data[p_key] = p_value
#     last_url = last_url[last_url.index("?")+1:len(last_url)]
#     #把last_url的字符串格式加到last_data字典
#     lis = last_url.split("&")
#     for a in lis:
#         last_data[a[0:a.index("=")]] = a[a.index("=")+1:len(a)]
#     #热加载替换
#     last_data = RequestUtil(Test()).replace_get_value(last_data)
#     #字典根据key的asccii码排序
#     new_dict = self.dict_asscii_sort(last_data)
#     #第二步：(2)把参数名和参数的值用=连接成字符串，多个参数之间用&连接。a=2&b=1&c=3
#     new_str = ""
#     for key,value in new_dict.items():
#         new_str = new_str+key+"="+value+"&"
#     #第三到第五步
#     appid = "wx8a9de038e93f77ab"
#     appsecret = "8326fc915928dee3165720c910effb86"
#     nonce = str(random.randint(1000000000,9999999999))
#     timestamp = str(time.time())
#     all_str = appid+appsecret+new_str+nonce+timestamp
#     #第六步
#     sign_str = self.md5(all_str)
#     return sign_str

#字典的key根据asscii排序
def dict_asscii_sort(self,dict_str):
    dict_key = dict(dict_str).keys()
    l = list(dict_key)
    l.sort()
    new_dict = {}
    for key in l:
        new_dict[key] = dict_str[key]
    return new_dict

#------------------------------自定义加密接口-------------------------------
#自定义返回json接口
@app.route('/api', methods=['GET','POST'])
def index():
    return {"mashang":[{"name":"百里","age":"13","student":[{"name":"张三","class":"210"},{"name":"李四","class":"210"},{"name":"王五","class":"210"}]},
                       {"name":"星瑶","arg":"11","student":[{"name":"马六","class":"211"},{"name":"赵七","class":"211"}]},
                       {"name":"依然","age":"12"}],
            "jiaoyu":"123"}

#模拟带参数的请求(md5加密的接口)
@app.route('/md5login',methods=['GET','POST'])
def md5login():
    username = request.values.get("username")
    password = request.values.get("password")
    if username==md5_jm("admin")and password==md5_jm("123"):
        return {"error_code":0,"message":"MD5加密登陆成功！"}
    else:
        return {"error_code":101,"message":"MD5加密登陆失败"}

#模拟带参数的请求(base64加密的接口)
@app.route('/base64login',methods=['GET','POST'])
def base64login():
    username = request.values.get("username")
    password = request.values.get("password")
    if username==base64_jm("admin") and password==base64_jm("123"):
        return {"error_code":0,"message":"Base64加密登陆成功！"}
    else:
        return {"error_code":101,"message":"Base64加密登陆失败"}

#模拟带参数的请求(base64加密的接口)
@app.route('/rsalogin',methods=['POST'])
def rsalogin():
    username = request.values.get("username")
    password = request.values.get("password")
    if rsa_jiemi(username)=="admin" and rsa_jiemi(password)=="123":
        return {"error_code":0,"message":"RSA加密登陆成功！"}
    else:
        return {"error_code":101,"message":"RSA加密登陆失败"}

if __name__ == '__main__':
    app.run()
    #app.run(host='0.0.0.0')
    #https://gitee.com/Aletto/Postman-encryption/raw/master/forge.js