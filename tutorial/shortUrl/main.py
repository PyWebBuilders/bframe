import base64
import random
import threading
import time
from urllib.parse import unquote

from bframe import Frame, Redirect, request

app = Frame(__name__)

base_server = "http://127.0.0.1:7256"
url_dict = dict()
url_lock = threading.Lock()


def insert_url(value):
    global url_dict
    key = generate_random_key()
    while_max = 10000
    with url_lock:
        while True:
            if while_max <= 0:
                raise Exception("程序异常")
            if key not in url_dict:
                url_dict[key] = value
                return key
            key = generate_random_key()
            while_max -= 1


def find_url(key):
    if key in url_dict:
        return url_dict[key]
    raise Exception("数据不存在")


def generate_random_key():
    key = "%s_%s_%s" % (time.time(), random.randint(0, 10), time.time())
    return base64.b64encode(key.encode()).decode()


@app.route("/", method=["GET", "POST"])
def index():
    if request.method == "GET":
        if "key" not in request.args:
            return "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <title>短连接生成器</title>\n</head>\n<body>\n<form action=\"/\" method=\"post\">\n    <label>\n        <input type=\"text\" name=\"url\"/>\n    </label>\n    <input type=\"submit\" value=\"提交\">\n</form>\n</body>\n</html>"
        key = request.args.get("key")
        return Redirect(find_url(key))
    if request.method == "POST":
        redirect_url = unquote(request.forms.get("url"))
        key = insert_url(redirect_url)
        return "%s/?key=%s" % (base_server, key)


if __name__ == "__main__":
    app.run()
