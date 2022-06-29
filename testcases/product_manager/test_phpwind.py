import json
import random
import re

import pytest
import requests

from commons.request_util import RequestUtil
from commons.yaml_util import write_yaml, read_yaml


class TestApi:

    pass

    # @pytest.mark.parametrize("caseinfo",read_testcase_yaml("testcases/product_manager/phpwind_index.yaml"))
    # def test_index(self,caseinfo):
    #     names = caseinfo["name"]
    #     methods = caseinfo["request"]["method"]
    #     urls = caseinfo["request"]["url"]
    #     validates = caseinfo["validate"]
    #
    #     res = RequestUtil().send_all_request(method=methods,url=urls)
    #     result = res.text
    #     #正则匹配body中的值
    #     data = {"csrf_token":re.search('name="csrf_token" value="(.*?)"',result).group(1)}
    #     write_yaml("extract.yaml",data)
    #
    # @pytest.mark.parametrize("caseinfo",read_testcase_yaml("testcases/product_manager/phpwind_login.yaml"))
    # def test_login(self,caseinfo):
    #     names = caseinfo["name"]
    #     methods = caseinfo["request"]["method"]
    #     urls = caseinfo["request"]["url"]
    #     headers = caseinfo["request"]["headers"]
    #     datas = caseinfo["request"]["data"]
    #     datas["csrf_token"] = read_yaml("extract.yaml","csrf_token")
    #     validates = caseinfo["validate"]
    #
    #     res = RequestUtil().send_all_request(method=methods,url=urls,data=datas,headers=headers)
    #     result = res.text
    #     print(result,type(result))