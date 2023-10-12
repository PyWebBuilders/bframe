<div align=center><img src="docs/favicon.ico"></div>


`bframe`是一个基于`WSGI`的协议的`web`框架。它非常像`flask`，但也会有`django restframework`的味道。

`bframe`的初衷是为了学习`python`的`web`框架，加深对`WSGI`及周边生态的了解。当然，若您想更深入的了解`python web`开发，请参与进来吧！


### 安装

```shell
pip install -U bframe
```

### 快速入门

```python
# app.py
from bframe import Frame

app = Frame(__name__)


@app.get("/")
def home():
    return "hello world"


if __name__ == "__main__":
    app.run()
```

### 启动项目

```shell
python app.py
```

### LINKS

项目文档: [https://bean-jun.github.io/bframe-docs/](https://bean-jun.github.io/bframe-docs/)

项目DEMO: [https://github.com/PyWebBuilders/Plats.git](https://github.com/PyWebBuilders/Plats.git)
