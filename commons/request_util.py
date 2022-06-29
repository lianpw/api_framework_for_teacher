import json
import re
import traceback
import jsonpath
import requests
from commons.assert_utils import assert_result
from commons.logger_util import print_log, error_log
from commons.yaml_util import write_yaml, read_yaml

class RequestUtil:

    sess = requests.session()

    def __init__(self,obj):
        self.obj = obj

    #规范YAML测试用例（用例的标准化）
    def standard_yaml_testcase(self,caseinfo):
        try:
            print_log("----------接口测试开始----------")
            caseinfo_keys = caseinfo.keys()
            #在YAML用例里面必须包含有一级关键字：name,request,validate
            if "name" in caseinfo_keys and "request" in caseinfo_keys and "validate" in caseinfo_keys:
                request_keys = caseinfo["request"].keys()
                print_log("接口名称：%s" % caseinfo["name"])
                #在YAML用例里面必须包含有一级关键字：name,request,validate
                if "method" in request_keys and "url" in request_keys and "base_url" in request_keys:
                    #发送请求
                    method = caseinfo["request"].pop("method") #删除method并返回method值
                    base_url = caseinfo["request"].pop("base_url")  # 删除url并返回url的值
                    url = caseinfo["request"].pop("url")#删除url并返回url的值
                    res = self.send_all_request(method,base_url,url,**caseinfo["request"])
                    text_result = res.text      #获得文本格式返回结果
                    status_code = res.status_code  #获得返回状态码
                    json_result = ""
                    try:
                        json_result = res.json()  # 获得josn格式返回结果
                    except:
                        print_log("返回的结果不是json数据格式!")
                    #提取需要关联的值并写入extract.yaml文件
                    if "extract" in caseinfo.keys():
                        for key,value in caseinfo["extract"].items():
                            if "(.*?)" in value or "(.+?)" in value:  #正则提取,支持文本
                                zz_value = re.search(value,text_result)
                                if zz_value:
                                    data = {key:zz_value.group(1)}
                                    write_yaml("extract.yaml",data)
                                else:
                                    pass
                                    #print("extract提取中间变量，正则写法有误或者接口返回有误！")
                            else:      #jsonpath提取，仅支持json格式数据
                                js_value = jsonpath.jsonpath(json_result,value)
                                if js_value:
                                    data = {key: js_value[0]}
                                    write_yaml("extract.yaml", data)
                                else:
                                    pass
                                    #print("extract提取中间变量，JSONPATH写法有误或者接口返回有误！")
                    # 断言：
                    yq_result = caseinfo["validate"]   #预期结果
                    sj_result = json_result             #实际结果
                    print_log("预期结果：%s" % yq_result)
                    print_log("实际结果：%s" % sj_result)
                    assert_result(yq_result,sj_result,status_code)
                    print_log("接口测试成功")
                    print_log("----------接口测试结束----------\n")
                else:
                    error_log("request下面必须包含有method,base_url,url这三个二级关键字")
                    print_log("----------接口测试结束----------\n")
            else:
                error_log("在YAML用例里面必须包含有一级关键字：name,request,validate")
                print_log("----------接口测试结束----------\n")
        except Exception as e:
            error_log("规范YAML测试用例报错：%s" % str(e))
            print_log("----------接口测试结束----------\n")
            raise e

    #统一请求封装（必做）
    def send_all_request(self,method,base_url,url,**kwargs):
        try:
            print_log("请求方式：%s" % method)
            #method统一小写
            method = str(method).lower()
            #url通过${变量名}取值
            url = self.replace_get_value(base_url+url)
            print_log("请求路径：%s" % url)
            #headers,params,data,json通过${变量名}取值
            for key,value in kwargs.items():
                if key in ["headers","params","data","json"]:
                    kwargs[key] = self.replace_get_value(value)
                    print_log("请求"+key+"参数：%s" % kwargs[key])
                elif key=="files":
                    for file_key,file_value in value.items():
                        value[file_key] = open(file_value,"rb")
            #发送请求
            res = RequestUtil.sess.request(method, url,**kwargs)
            return res
        except Exception as e:
            error_log("发送请求报错：%s" % str(e))
            raise e

    #封装替换取值的方法
    #注意1：取值可能是（url,params,data,json,headers）
    #注意2：各种数据类型的切换：(int,float,string,list,dict)
    def replace_get_value(self,data):
        try:
            if data:
                #保存传入的数据的类型
                data_type = type(data)
                #把不同的数据类型转化成字符串，因为只有字符串才能替换。
                if isinstance(data,list) or isinstance(data,dict):
                    str_data = json.dumps(data)
                else:
                    str_data = str(data)
                #替换
                for a in range(1,str_data.count("${")+1):
                    if "${" in str_data and "}" in str_data:
                        start_index = str_data.index("${")
                        end_index = str_data.index("}",start_index)
                        old_value = str_data[start_index:end_index+1]
                        #print(old_value)
                        #反射getattr：通过【类的对象】和【方法名】字符串调用方法
                        #通过old_value得到方法名
                        functon_name = old_value[2:old_value.index("(")]
                        #print("functon_name：%s"%functon_name)
                        #通过old_value得到参数的值
                        args_value = old_value[old_value.index("(")+1:old_value.index(")")]
                        #print("args_value: %s"%args_value)
                        #判断此函数是否有参数，如果args_value!=""代表有参数。
                        if args_value!="":
                            #有参数
                            #分割参数
                            all_args_value = args_value.split(",")
                            new_value = getattr(self.obj, functon_name)(*all_args_value)
                            #print(new_value)
                        else:
                            #没有参数
                            # 调用反射方法获得方法的放回值
                            new_value = getattr(self.obj,functon_name)()
                            #print(new_value)
                        #把旧的表达式替换成返回的新的值
                        if isinstance(new_value,int) or isinstance(new_value,float):
                            str_data = str_data.replace('"'+old_value+'"', str(new_value))
                        else:
                            str_data = str_data.replace(old_value,str(new_value))
                #还原数据类型
                if isinstance(data,list) or isinstance(data,dict):
                    data = json.loads(str_data)
                else:
                    data = data_type(str_data)
                #返回值
                return data
            else:
                #print("None不需要通过${变量名}取值")
                return data
        except Exception as e:
            error_log("热加载替换值报错：%s" % str(e))
            raise e