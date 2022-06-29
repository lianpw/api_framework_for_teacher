import os
import random
import yaml

class Test:

    def get_randoms(self):
        return str(random.randint(10000,99999))

    def read_extract(self,key):
        with open(os.getcwd() + "/extract.yaml", mode="r", encoding="utf-8") as f:
            result = yaml.load(stream=f, Loader=yaml.FullLoader)
            return result[key]

    # 获取基础路径
    def read_config(self, node_key):
        with open(os.getcwd() + "/config.yaml", mode="r", encoding="utf-8") as f:
            result = yaml.load(stream=f, Loader=yaml.FullLoader)
            return result[node_key]