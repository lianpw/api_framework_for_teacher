#读取测试用例的yaml文件
import json
import traceback

import yaml

from commons.logger_util import print_log, error_log
from commons.yaml_util import get_object_path

#读取测试用例
def read_testcase_yaml(yaml_path):
    try:
        with open(get_object_path()+"/"+yaml_path,mode="r",encoding="utf-8") as f:
            caseinfo = yaml.load(stream=f, Loader=yaml.FullLoader)
            if len(caseinfo)>=2:   #表示通过复制yaml的内容实现数据驱动
                return caseinfo
            else:
                if "parameterize" in dict(*caseinfo).keys():
                    #需要解析parameterize数据驱动
                    new_caseinfo = parameterize_ddt(*caseinfo)
                    return new_caseinfo
                else:
                    return caseinfo
    except Exception as e:
        error_log("读取测试用例的YAML文件报错：%s" % str(e))
        raise e

#解析parameterize数据驱动
def parameterize_ddt(caseinfo):
    try:
        caseinfo_str = json.dumps(caseinfo)
        data_list = caseinfo["parameterize"]
        #规范数据驱动的写法
        length_success = True
        key_length = len(data_list[0])
        for param in caseinfo["parameterize"]:
            if len(param)!=key_length:
                length_success = False
                error_log("此条数据有误：%s"%param)
                continue
        #替换值
        new_caseinfo = []
        if length_success:
            for x in range(1,len(data_list)):  #行
                raw_caseinfo = caseinfo_str
                for y in range(0,len(data_list[x])):
                    #判断如果是int或者float那么需要处理一下
                    if isinstance(data_list[x][y],int) or isinstance(data_list[x][y],float):
                        raw_caseinfo = raw_caseinfo.replace('"$ddt{' + data_list[0][y] + '}"', str(data_list[x][y]))
                    else:
                        raw_caseinfo=raw_caseinfo.replace("$ddt{"+data_list[0][y]+"}",str(data_list[x][y]))
                new_caseinfo.append(json.loads(raw_caseinfo)) #把每一行的字典追加到new_caseinfo里面
        #返回解析之后的测试用例
        return new_caseinfo
    except Exception as e:
        error_log("数据驱动DDT报错：%s" % str(traceback.format_exc()))
        raise e