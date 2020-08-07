from baseapi.baseapi import baseapi
from baseapi.pubilc import public


class Tagapi(baseapi):
    corpsecret = baseapi.load_yml("./yaml/token.yml")["corpsecret"]

    def __init__(self):
        baseapi.__init__(self)
        self.token = public().get_token(self.corpsecret)


    def add_tag(self, **data):
        data.update({"token": self.token})
        # 更新字典内容
        # x={"a":1}
        # y={"b":2}
        # x.update(y)
        # x-> {"a":1,"b":2}
        add_tag = baseapi.template("./yaml/tag/add_tag.yml", data)
        return self.interface_api(add_tag)

    def delete_tag(self, **data):
        data.update({"token": self.token})
        data = self.template('./yaml/tag/tag.all.yaml', data, sub="delete")
        return self.interface_api(data)

    def alter_tag(self, **data):
        data.update({"token": self.token})
        alter_tag = baseapi.template("./yaml/tag/tag.all.yaml", data, sub="alter")
        return self.interface_api(alter_tag)

    def get_tag(self):
        get_tag = baseapi.load_yml("./yaml/tag/get_tag.yml")
        get_tag['params']['access_token'] = self.token
        return self.interface_api(get_tag)
