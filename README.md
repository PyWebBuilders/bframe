# A simple python web server frame

> `wranning`: same flask, not flask!

### demo

-> main.py


### web server 自定义协议

```python
from simple_server.frame import Frame
from simple_server.http_server import Request

app = Frame(__name__)


@app.get("/favicon.ico")
def index(request: Request):
    with open("favicon.ico", "rb") as f:
        data = f.read()
    return data


@app.get("/main")
@app.get("/home")
def home(request: Request):
    return request.Headers


if __name__ == "__main__":
    app.run(address="0.0.0.0")
```

### wsgi支持

若您需要使用wsgi功能的支持，使用`wsgi_proxy`进行包装即可

```python
from simple_server.frame import Frame
from simple_server.http_server import Request

app = Frame(__name__)


@app.get("/favicon.ico")
def index(request: Request):
    with open("favicon.ico", "rb") as f:
        data = f.read()
    return data


@app.get("/main")
@app.get("/home")
def home(request: Request):
    return request.Headers


if __name__ == "__main__":
    from simple_server.wsgi_server import wsgi_proxy
    from wsgiref.simple_server import make_server

    with make_server('', 7256, wsgi_proxy(app)) as httpd:
        print("Serving on port 7256...")
        httpd.serve_forever()
```