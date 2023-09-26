### wsgi支持

若您需要使用wsgi功能的支持，使用`WSGIProxy`类进行包装即可

```python
from bframe import WSGIProxy
from wsgiref.simple_server import make_server

with make_server('', 7256, WSGIProxy(app)) as httpd:
    print("Serving on port 7256...")
    httpd.serve_forever()
```


### 添加钩子支持


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


### 支持重定向

```python
from bframe import Redirect, request

@app.get("/short_url")
def short_url():
    return Redirect(request.args.get("returnUrl"))
```

### 支持g变量

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

### 解析请求体

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

### 支持路径参数匹配(字符串、数字、正则)

```python
@app.get("/api/<reg:(?P<version>v\d+$)>/user/<int:pk>")
def user_api(version, pk):
    return {"api_version": version, "path_args": pk}
```

### 支持静态文件

```python
app = Frame(__name__, static_url="static", static_folder="static")
```

### 支持解析py配置文件

```python
app.Config.from_py("config")
```

### 支持cookie&session操作

```python
from bframe import Frame
from bframe import make_response
from bframe import session

app = Frame(__name__)

@app.get("/")
def index():
    ret = make_response("hello world")
    sess["username"] = "tom"
    ret.set_cookies("x-username", "tom", path="/")
    return ret


@app.get("/home")
def home():
    username = sess["username"]
    if not username:
        return "not login"
    print(request.Cookies.get("x-username"))
    ret = make_response("home")
    return ret


if __name__ == "__main__":
    app.run()
```

### 支持类视图

```python
from bframe import MethodView

app = Frame(__name__)

class BookView(MethodView):

    def get(self):
        return books

    def post(self):
        global books
        req = request.forms
        req['id'] = len(books) + 1
        books.append(req)
        return req


app.add_route("/book", BookView.as_view())


if __name__ == "__main__":
    app.run()
```

### 支持通用类视图&默认路由

```python
from bframe.serizlizer import SimpleSerializer
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()


class Phone(Base):
    __tablename__ = 'phones'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)


# Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()



class PhoneViewSet(ViewSet):
    decorators = [prue_response_decorator]
    table_class = Phone
    table_serializer = SimpleSerializer

    def get_session(self):
        return session



# ================================
app.add_route("/phone", PhoneViewSet.as_view({
    "get": "list",
    "post": "create",
}))
app.add_route("/phone/<int:pk>", PhoneViewSet.as_view({
    "get": "retrieve",
    "post": "update",
    "put": "partial_update",
    "delete": "destroy",
}))
# 或者================================
from bframe.generics import DefaultRouter

router = DefaultRouter(app)
# PhoneViewSet
router.register("/phone", PhoneViewSet)


if __name__ == "__main__":
    app.run()
```

### 框架默认配置

```shell
# session相关的默认配置
"SESSION_ID": "_session"
"SESSION_MAX_AGE": 604800  # a week
"SESSION_EXPIRES": None
"SESSION_PATH": "/"
"SESSION_DOMAIN": None
"SESSION_SECURE": False
"SESSION_HTTPONLY": True
"SESSION_SAMESITE": None

# 通用视图默认配置
"GENERIC_VIEW_DEFAULT_PRIMARY_KEY": "id"                  # 数据库主键名称
"GENERIC_VIEW_DEFAULT_LIMIT": 20                          # 默认查询总量
"GENERIC_VIEW_DEFAULT_LIMIT_KEY": "_limit"                # 默认查询总量key
"GENERIC_VIEW_DEFAULT_OFFSET": 1                          # 默认分页数
"GENERIC_VIEW_DEFAULT_OFFSET_KEY": "_offset"              # 默认分页数key
"GENERIC_VIEW_DEFAULT_ORDER_BY": "id"                     # 数据查询排序字段
"GENERIC_VIEW_DEFAULT_ORDER_BY_KEY": "_order_by"          # 数据查询排序字段key
"GENERIC_VIEW_DEFAULT_ORDER": "asc"                       # 数据查询排序字段顺序
"GENERIC_VIEW_DEFAULT_ORDER_KEY": "_order"                # 数据查询排序字段顺序key
```
