import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from bframe import Frame
from bframe import g, request, abort, current_app
from bframe import MethodView
from bframe import make_response
from bframe.yellowprint import YellowPrint

app = Frame(__name__)
app.Config.from_py("_frame_config.py")
yellow01_app = YellowPrint("yellow01")
yellow02_app = YellowPrint("yellow02")
app.register_yellowprint(yellow01_app)
app.register_yellowprint(yellow02_app)


@yellow02_app.add_before_app_handle
def yellow02_before_001():
    user = request.args.get("user")
    if not user:
        return {
            "code": 200,
            "status": False,
            "msg": "未登录"
        }


@yellow01_app.get("/")
def yellow01_index():
    return "hello yellow01 api"


@yellow02_app.get("/")
def yellow02_index():
    return "hello yellow02 api"


@app.get("/")
@app.get("/index")
def index():
    return "hello world"


@app.get("/conf")
def conf():
    return dict(current_app.Config)


@app.route("/login", method=["POST"])
def login():
    user = request.forms.get("user")
    pwd = request.forms.get("pwd")
    if not all([user, pwd]):
        return {
            "code": 200,
            "status": False,
            "msg": "数据不完整"
        }
    if user != 'admin' or pwd != "admin":
        return {
            "code": 200,
            "status": False,
            "msg": "账号密码异常"
        }

    data = {
        "code": 200,
        "status": True,
        "msg": "登录成功"
    }
    resp = make_response(body=data)
    resp.set_cookies("username", user)
    return resp


@app.get("/admin")
def admin():
    if not g.user:
        abort(401)
    return {
        "code": 200,
        "status": True,
        "msg": "获取后台数据成功",
        "cookie": {
            k: request.Cookies[k].value for k in request.Cookies.keys()
        }
    }


@app.get("/api/user/<str:username>/profile")
def users(username):
    return {
        "code": 200,
        "status": True,
        "msg": "获取后台数据成功",
        "data": {
            "username": username
        }
    }


@app.get("/admin/api/users/<int:uid>/profile")
def users(uid):
    return {
        "code": 200,
        "status": True,
        "msg": "获取后台数据成功",
        "data": {
            "user_id": uid
        }
    }


@app.add_before_handle
def before_auth():
    user = request.args.get("user")
    g.user = user


@app.add_error_handle(401)
def error_401():
    return {
        "code": 401,
        "status": False,
        "msg": "小伙子，请登录一下吧"
    }


class UserInfo(MethodView):

    def return_value(self, value):
        return {
            "code": 200,
            "status": True,
            "msg": "获取后台数据成功",
            "data": {
                "userinfo": value
            }
        }

    def get(self):
        return self.return_value("get")

    def post(self):
        return self.return_value("post")

    def put(self):
        return self.return_value("put")

    def delete(self):
        return self.return_value("delete")


app.add_route("/userinfo", UserInfo.as_view())
yellow01_app.add_route("/userinfo", UserInfo.as_view())


if __name__ == "__main__":
    app.run()
