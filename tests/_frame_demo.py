import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bframe import Frame
from bframe import g, request, abort, current_app


app = Frame(__name__)
app.Config.from_py("_frame_config.py")

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
    
    return {
        "code": 200,
        "status": True,
        "msg": "登录成功"
    }


@app.get("/admin")
def admin():
    if not g.user:
        abort(401)
    return {
        "code": 200,
        "status": True,
        "msg": "获取后台数据成功"
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


if __name__ == "__main__":
    app.run()
