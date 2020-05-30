from pprint import pprint
from string import Template

import requests
import yaml
from jsonpath import jsonpath

from util.log import log


class baseapi:
    def __init__(self):
        self.mylog = log()

    def interface_api(self, req: dict):
        # 使用 request 完成多请求的改造（post, get, delete）
        # pprint(req)
        r = requests.request(**req)
        pprint(r.json())
        self.mylog.info("请求日志:" + yaml.dump(r.json()))
        return r.json()

    @classmethod
    def base_jsonpath(cls, json, expr):
        return jsonpath(json, expr)

    @classmethod
    def load_yml(cls, path):
        with open(path) as f:
            return yaml.safe_load(f)

    @classmethod
    def template(cls, path, data, sub=None):
        with open(path, 'r') as f:
            if sub is None:
                return yaml.load(Template(f.read()).substitute(data))
            else:
                # return yaml.load(Template(f.read()).substitute(data))[sub]
                return yaml.load(Template(yaml.dump(yaml.load(f)[sub])).substitute(data))
