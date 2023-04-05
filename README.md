# A simple python web server frame

> `wranning`: same flask, not flask!


### use

```shell
pip install bframe -i https://pypi.org/simple
```

or 

```shell
git clone https://github.com/Bean-jun/bframe.git
python setup.py install
```

### demo

-> main.py


### web server 自定义协议

```python
from bframe import request
from bframe import Frame


app = Frame(__name__)


@app.get("/favicon.ico")
def index():
    with open("favicon.ico", "rb") as f:
        data = f.read()
    return data


@app.get("/main")
@app.get("/home")
def home():
    url = request.Args.get("url")
    if url:
        return Redirect(url)
    return request.Headers


if __name__ == "__main__":
    app.run(address="0.0.0.0")
```

### wsgi支持

若您需要使用wsgi功能的支持，使用`WSGIProxy`类进行包装即可

```python
from bframe import request
from bframe import Frame


app = Frame(__name__)


@app.get("/favicon.ico")
def index():
    with open("favicon.ico", "rb") as f:
        data = f.read()
    return data


@app.get("/main")
@app.get("/home")
def home():
    url = request.Args.get("url")
    if url:
        return Redirect(url)
    return request.Headers


if __name__ == "__main__":
    from bframe import WSGIProxy
    from wsgiref.simple_server import make_server

    with make_server('', 7256, WSGIProxy(app)) as httpd:
        print("Serving on port 7256...")
        httpd.serve_forever()
```


### 添加钩子支持


1. 定义请求钩子 

    ```python
    # 定义请求钩子
    @app.add_before_handle
    def before_02():
        if request.Method == "POST":
            return "disallow method"
    ```
2. 定义响应钩子 

    ```python
    # 定义响应钩子
    @app.add_after_handle
    def after_xx(resp: Response):
        print("resp:", resp.Code)
        return resp
    ```
3. 自定义错误响应 

    ```python
    # 自定义错误响应
    @app.add_error_handle(401)
    def err_401():
        return "401 error"
    ```


### 支持重定向

### 支持g变量

### 解析请求体