import pystache

class Template:
    @classmethod
    def render(cls, path, dict):
        render = pystache.Renderer(escape=lambda u: u)
        with open(path) as f:
            content = f.read()
            parsed = pystache.parse(content)
            print(parsed)
            print("测试打印")
            result = render.render(parsed, dict)
            print(result)
            return result