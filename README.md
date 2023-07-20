# A simple python web server frame

> `Please do not use in a production environment!`
> 
> `wranning`: same flask, not flask!


### 1. 快速安装使用

```shell
pip install bframe -i https://pypi.org/simple
```

or 

```shell
git clone https://github.com/Bean-jun/bframe.git
python setup.py install
```

### 2. 快速入门

```python
from bframe import Frame

app = Frame(__name__)


@app.get("/")
@app.get("/index")
def home():
    return "hello world"


if __name__ == "__main__":
    app.run()
```

### 3. wsgi支持

若您需要使用wsgi功能的支持，使用`WSGIProxy`类进行包装即可

```python
from bframe import WSGIProxy
from wsgiref.simple_server import make_server

with make_server('', 7256, WSGIProxy(app)) as httpd:
    print("Serving on port 7256...")
    httpd.serve_forever()
```


### 4. 添加钩子支持


定义请求钩子 

```python
# 定义请求钩子
@app.add_before_handle
def before_01():
    if request.Method == "POST":
        return "disallow method"
```

定义响应钩子 

```python
# 定义响应钩子
@app.add_after_handle
def after_01(resp: Response):
    print("resp:", resp.Code)
    return resp
```

自定义错误响应 

```python
# 自定义错误响应
@app.add_error_handle(401)
def err_401():
    return "401 error"
```


### 5. 支持重定向

```python
from bframe import Redirect, request

@app.get("/short_url")
def short_url():
    return Redirect(request.args.get("returnUrl"))
```

### 6. 支持g变量

```python
from bframe import Frame, g, request

app = Frame(__name__)


@app.add_before_handle
def before_01():
    username = request.Headers.get("username")
    g.username = username

@app.get("/profile")
def profile():
    return {"username": g.username}
```

### 7. 解析请求体

```python
from bframe import request


@app.route("/", ["get", "post"])
def index():
    print({"args": request.args,
           "forms": request.forms,
           "files": request.files,
           })
    return "ok"
```

### 8. 支持路径参数匹配(字符串、数字、正则)

```python
@app.get("/api/<reg:(?P<version>v\d+$)>/user/<int:pk>")
def user_api(version, pk):
    return {"api_version": version, "path_args": pk}
```

### 9. 支持静态文件

```python
app = Frame(__name__, static_url="static", static_folder="static")
```

### 10. 支持解析py配置文件

```python
app.Config.from_py("config")
```

### 11. 样例参考

> `main.py`
> 
> [https://github.com/Bean-jun/Plats.git](https://github.com/Bean-jun/Plats.git)
