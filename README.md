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

### 2. 样例demo

> `main.py`
> 
> [https://github.com/Bean-jun/Plats.git](https://github.com/Bean-jun/Plats.git)


### 3. 快速使用

```python
from bframe import request, Redirect
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

### 4. wsgi支持

若您需要使用wsgi功能的支持，使用`WSGIProxy`类进行包装即可

```python
from bframe import request, Redirect
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


### 4. 添加钩子支持


定义请求钩子 

```python
# 定义请求钩子
@app.add_before_handle
def before_02():
    if request.Method == "POST":
        return "disallow method"
```

定义响应钩子 

```python
# 定义响应钩子
@app.add_after_handle
def after_xx(resp: Response):
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

### 6. 支持g变量

### 7. 解析请求体

### 8. 支持路径参数匹配(字符串、数字、正则)

### 9. 支持静态文件

### 10. 支持解析py配置文件