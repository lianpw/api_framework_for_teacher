import traceback
import jsonpath
from commons.database_util import DatabaseUtil
from commons.logger_util import print_log, error_log

def assert_result(yq_result,sj_result,status_code):
    try:
        all_flag = 0
        if yq_result:
            for yq in yq_result:
                for key,value in yq.items():
                    if key=="codes":
                        # print("返回码断言")
                        flag = codes_assert(value,status_code)
                        all_flag = all_flag + flag
                    elif key=="equals":
                        # print("相等断言")
                        flag = equals_assert(value,sj_result)
                        all_flag = all_flag + flag
                    elif key=="contains":
                        # print("包含断言")
                        flag = contains_assert(value, sj_result)
                        all_flag = all_flag + flag
                    elif key=="db_equals":
                        # print("数据库断言")
                        flag = database_assert(value, sj_result)
                        all_flag = all_flag + flag
                    else:
                        error_log("框架不支持此断言方式！")
        else:
            all_flag = -1
        #########判断断言结果#########
        if all_flag == 0:
            pass
            #print_log("结果断言成功！")
        elif all_flag == -1:
            pass
            #print_log("没有断言！")
        else:
            error_log("结果断言失败")
            assert 1==2
    except Exception as e:
        error_log("断言报错：%s" % str(traceback.format_exc()))
        raise e

#状态码断言
def codes_assert(value,status_code):
    flag = 0
    for assert_key,assert_value in value.items():
        if assert_key=="status_code":
            if assert_value!=status_code:
                flag = flag + 1
                print_log("codes断言失败："+str(assert_key)+"不等于"+str(assert_value)+"")
    return flag

#相等断言
def equals_assert(value,sj_result):
    flag = 0
    for assert_key,assert_value in value.items():
        lists = jsonpath.jsonpath(sj_result,'$..%s'%assert_key)
        if lists:
            if assert_value not in lists:
                flag = flag + 1
                error_log("equals断言失败："+str(assert_key)+"不等于"+str(assert_value)+"")
        else:
            flag = flag + 1
            error_log("equals断言失败：返回的结果中没有"+str(assert_key)+"")
    return flag

#包含断言
def contains_assert(value,sj_result):
    flag = 0
    if str(value) not in str(sj_result):
        flag = flag + 1
        error_log("contains断言失败：返回结果中没有"+str(value)+"")
    return flag

#数据库断言
def database_assert(value,sj_result):
    flag = 0
    for sql,key in value.items():
        #判断实际结果中是否包含有key
        lists = jsonpath.jsonpath(sj_result, '$..%s' % key)
        if lists:
            res = None
            try:
                res = DatabaseUtil().execute_sql(sql)
            except:
                flag = flag + 1
                error_log("db_equals断言失败：SQL查询异常或有语法错误：%s" % str(traceback.format_exc()))
                break
            print(res)
            # 如果res=None说明要么就是SQL语句有误，或者是没有查询到结果。
            if not res:
                flag = flag + 1
                error_log("db_equals断言失败：查询没有结果返回")
            else:
                # 判断
                if lists[0] == res[0]:
                    error_log("数据库断言成功")
                else:
                    flag = flag + 1
                    error_log("db_equals断言失败：SQL查询结果不等于实际结果")
        else:
            flag = flag + 1
            error_log("db_equals断言失败：实际结果中不包含" + str(key) + "")
    return flag
