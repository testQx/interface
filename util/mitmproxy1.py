import os
import sys
sys.path.append('/Users/bytedance/Library/Python/3.8/lib/python/site-packages')
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages')
addon_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(addon_dir)
from util.Template import Template
from mitmproxy import http


def response(flow: http.HTTPFlow):
    if ".json" in flow.request.pretty_url:
        method = flow.request.method
        url = flow.request.pretty_url.split('?')[0]
        params = [{k: v} for k, v in flow.request.query.fields]
        cookies = [{k: v} for k, v in flow.request.cookies.fields]
        data = {
            "method": method.__repr__(),
            "url": url.__repr__(),
            "params": params,
            "cookies": cookies
        }
        json_data=Template.render(addon_dir + "/util/test_http.mustache", data)
        print(json_data)
        with open("/Users/bytedance/Documents/lfq/interface/util/test_mitm.py","a") as f:
            f.write(json_data)
        # print(mustache.template(path=(addon_dir + "/util/test_http.mustache"), data=data))

os.system('mitmdump -s /Users/bytedance/Documents/lfq/interface/util/mitmproxy1.py')
