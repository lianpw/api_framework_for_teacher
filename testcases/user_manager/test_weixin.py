import json
import random
import re

import pytest
import requests

from commons.ddt_util import read_testcase_yaml
from commons.request_util import RequestUtil
from commons.yaml_util import write_yaml, read_yaml
from hotloads.debug_talk import DebugTalk
from hotloads.test import Test


class TestApi:

    access_token = ""
    csrf_token = ""

    # @pytest.mark.parametrize("caseinfo",read_testcase_yaml("testcases/user_manager/get_token.yaml"))
    # def test_get_token(self,caseinfo):
    #     RequestUtil(DebugTalk()).standard_yaml_testcase(caseinfo)

    # @pytest.mark.parametrize("caseinfo", read_testcase_yaml("testcases/user_manager/add_flag.yaml"))
    # def test_add_flag(self, caseinfo):
    #     RequestUtil(Test()).standard_yaml_testcase(caseinfo)
    #
    # @pytest.mark.parametrize("caseinfo",read_testcase_yaml("testcases/user_manager/edit_flag.yaml"))
    # def test_edit_flag(self,caseinfo):
    #     RequestUtil(Test()).standard_yaml_testcase(caseinfo)
    #
    # @pytest.mark.parametrize("caseinfo",read_testcase_yaml("testcases/user_manager/delete_flag.yaml"))
    # def test_del_flag(self,caseinfo):
    #     RequestUtil(DebugTalk()).standard_yaml_testcase(caseinfo)

    # @pytest.mark.parametrize("caseinfo", read_testcase_yaml("testcases/user_manager/select_flags.yaml"))
    # def test_select_flag(self, caseinfo):
    #     RequestUtil(DebugTalk()).standard_yaml_testcase(caseinfo)
    #
    # @pytest.mark.parametrize("caseinfo",read_testcase_yaml("testcases/user_manager/file_upload.yaml"))
    # def test_file_upload(self,caseinfo):
    #     RequestUtil(DebugTalk()).standard_yaml_testcase(caseinfo)

    # @pytest.mark.parametrize("caseinfo", read_testcase_yaml("testcases/user_manager/md5_case.yaml"))
    # def test_md5_case(self, caseinfo):
    #     RequestUtil(DebugTalk()).standard_yaml_testcase(caseinfo)
    #
    # @pytest.mark.parametrize("caseinfo", read_testcase_yaml("testcases/user_manager/base64_case.yaml"))
    # def test_base64_case(self, caseinfo):
    #     RequestUtil(DebugTalk()).standard_yaml_testcase(caseinfo)
    #
    # @pytest.mark.parametrize("caseinfo", read_testcase_yaml("testcases/user_manager/rsa_case.yaml"))
    # def test_rsa_case(self, caseinfo):
    #     RequestUtil(DebugTalk()).standard_yaml_testcase(caseinfo)

    @pytest.mark.parametrize("caseinfo", read_testcase_yaml("testcases/user_manager/sign_case.yaml"))
    def test_sign_case(self, caseinfo):
        RequestUtil(DebugTalk()).standard_yaml_testcase(caseinfo)