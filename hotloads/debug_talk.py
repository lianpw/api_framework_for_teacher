import base64
import hashlib
import os
import random
import time

import rsa
import yaml

from commons.request_util import RequestUtil


class DebugTalk:

    def get_random(self,min,max):
        return str(random.randint(int(min),int(max)))

    def read_extract(self,key):
        with open(os.getcwd() + "/extract.yaml", mode="r", encoding="utf-8") as f:
            result = yaml.load(stream=f, Loader=yaml.FullLoader)
            return result[key]

    #获取基础路径
    def read_config(self,node_key):
        with open(os.getcwd() + "/config.yaml", mode="r", encoding="utf-8") as f:
            result = yaml.load(stream=f, Loader=yaml.FullLoader)
            return result[node_key]

    #md5加密
    def md5(self,args):
        #以指定的编码格式编码字符串
        urf8_str = str(args).encode("utf-8")
        #md5加密
        md5_str = hashlib.md5(urf8_str).hexdigest()
        #返回
        return md5_str

    #base64加密
    def bs64(self,args):
        # 以指定的编码格式编码字符串
        urf8_str = str(args).encode("utf-8")
        # md5加密
        base64_str = base64.b64encode(urf8_str).decode("utf-8")
        # 返回
        return base64_str

    #RSA双钥加密
    #1.生成公钥和私钥
    # def create_keys(self):
    #     (public_key,private_key)  = rsa.newkeys(1024)
    #     #保存公钥
    #     with open("public.pem","w+") as f:
    #         f.write(public_key.save_pkcs1().decode())
    #     # 保存私钥
    #     with open("private.pem", "w+") as f:
    #         f.write(private_key.save_pkcs1().decode())

    #rsa加密
    def rsa_public_jiami(self,args):
        with open("./hotloads/public.pem",encoding="utf-8") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read().encode())
        #加密
        byte_str = rsa.encrypt(str(args).encode("utf-8"),public_key)
        #把字节转化成字符串
        miwen = base64.b64encode(byte_str).decode("utf-8")
        return miwen

    # rsa解密
    # def rsa_private_jiemi(self, args):
    #     with open("./hotloads/private.pem", encoding="utf-8") as f:
    #         private_key = rsa.PrivateKey.load_pkcs1(f.read().encode())
    #     #把一个字符串转化成字节类型
    #     byte_str = base64.b64decode(args)
    #     #解密
    #     mingwen = rsa.decrypt(byte_str,private_key).decode()
    #     print(mingwen)
    def signs(self,yaml_path):
        print(yaml_path)
        all_args_dict = {}   #定义的所有的参数字典
        #第一步：获得所有的参数，包括，url,params,data里面的参数
        with open(os.getcwd()+"/"+yaml_path,encoding="utf-8") as f:
            #加载yaml的内容
            yaml_content = yaml.load(f,Loader=yaml.FullLoader)
            #因为yaml_content是一个列表，这里对列表循环，得到测试用例字典
            for caseinfo in yaml_content:
                #得到测试用例字典里面所有的key
                caseinfo_keys = caseinfo.keys()
                #如果request在测试用例的key里面
                if "request" in caseinfo_keys:
                    #得到request的值
                    request_value =  caseinfo["request"]
                    print(request_value)
                    # 判断url是否在request的key里面，并打印
                    if "url" in request_value.keys():
                        url = request_value["url"]
                        #对url切片得到参数
                        url_args = url[url.index("?")+1:]
                        #对参数进行分割
                        args_list = str(url_args).split("&")
                        #把参数列表转化成参数字典
                        for args in args_list:
                            all_args_dict[args[0:args.index("=")]] = args[args.index("=")+1:]
                        #print(url_args_dict)
                    #判断params,data是否在request的key里面，并打印
                    for key,value in request_value.items():
                        if key in ["params","data"]:
                            for args_key,args_value in value.items():
                                all_args_dict[args_key] = args_value
                    #打印所有参数的字典
                    all_args_dict = self.dict_asccii_sort(all_args_dict)
                    print(all_args_dict)
                    #注意事项：如果说参数里面是带有${fucntion()}这种结构，那么这里需要调用替换方法
                    all_args_dict = RequestUtil(DebugTalk()).replace_get_value(all_args_dict)
                    print(all_args_dict)
        #第二步：
        new_str = ""
        for key,value in all_args_dict.items():
            new_str = new_str+str(key)+"="+str(value)+"&"
        new_str = new_str[0:-1]
        print(new_str)
        #第三-五步
        appid = "www"
        appsecret = "ccc"
        nonce = str(random.randint(1000000000,9999999999))
        timestamp = str(time.time())
        new_str = "appid="+appid+"&appsecret="+appsecret+"&"+new_str+"&nonce="+nonce+"&timestamp="+timestamp
        print(new_str)
        #第六步
        sign = self.md5(new_str).upper()
        print(sign)
        return sign

    #把字典安装key的Asccii码升序排序
    def dict_asccii_sort(self,args_dict):
        dict_key =  dict(args_dict).keys()
        l = list(dict_key)
        l.sort()
        new_dict = {}
        for key in l:
            new_dict[key] = args_dict[key]
        return new_dict

if __name__ == '__main__':
    pass
    #DebugTalk().create_keys()
    #print(DebugTalk().rsa_public_jiami("admin"))

    #print(DebugTalk().rsa_private_jiemi("HOeP2Fl2uodOWEtFTXjbXv9qjpKIwGiqdSaAUeewj7WHWfOnXgUjadGveWQbsAfvjaCK0nNcF1Ui1lwuVzgWVtSYDSeronm+csNs7uuGXLYIuts8IdBYXa++eBy01tlDNRYIJscPTvKc4VTr2JWJbHqZOhkOTs9elRMG/btY3sc="))
    #DebugTalk().md5("admin")
    #print(DebugTalk().get_random(10000,99999))