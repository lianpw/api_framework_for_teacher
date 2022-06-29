一、规范YAML测试用例的写法：
1.在YAML用例里面必须包含有一级关键字：name,request,validate，然后再request下面必须包含有method,url
这两个二级关键字。

二、关于接口关联
1.提取中间变量
    1).此框架仅支持正则表达式提取以及Jsonpath提取，并且表达式匹配的值只能有一个。
    2).提取的实例如下：extract是一级关键字
    extract:
        access_token1: '"access_token":"(.*?)"'
        access_token2: $.access_token
2.使用中间变量(可以在url,params,data,json,headers里面使用)
    ${read_extract(access_token)}

三、热加载
1.在hotloads里面新建一个py文件，并创建一个类，在类里面写方法
2.在YAML测试用例中通过以下方式调用方法实现热加载
${get_random(10000,99999)}






