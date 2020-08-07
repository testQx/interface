from baseapi.baseapi import baseapi


class public(baseapi):
    def get_token(self,corpsecret):
        corpid = self.load_yml("./yaml/token.yml")["corpid"]
        data = {
            "method": "get",
            "url": 'https://qyapi.weixin.qq.com/cgi-bin/gettoken',
            "params": {
                "corpid": corpid,
                "corpsecret": corpsecret
            }

        }
        return self.interface_api(data)['access_token']