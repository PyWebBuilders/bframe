<div align=center>
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="32px" height="32px" viewBox="0 0 32 32" enable-background="new 0 0 32 32" xml:space="preserve">  <image id="image0" width="32" height="32" x="0" y="0"
    href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAABGdBTUEAALGPC/xhBQAAACBjSFJN
AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QA/4ePzL8AAAAHdElN
RQfnCgwNFCDa60JNAAABNElEQVQoz3WRPUtCcRjFf89fy7o0BDaYUhQ0FWT3qoP5IRqKPkASNOTQ
FxBrbrG1Iell6QVaWgrChhTSdKtoaAlsjIYSjO7T0hUyO+PhcH4HjsDMrC+HhfJbok2Tq15jJ51S
YoQuikacop2U2LlJV57B2eVSLDJM8KQbtQMAO2wKBqvyDCDjssMSR+SJyJ6zCFBvYPnb7E9wM/Uy
xN7JyjyHAKjxiOqCvgAwBNQ8398eLeB7HesLrumK3PRu/QmoT+AsOMWgPH6tlpue30bQg3Kvm5rH
+Erxhb+IAO7tMoC9byqa57izIUDrB/YGDE/2djQwwAdAbFQLwNVdywtIO9AfO9Uwtvh5kLRHNtqM
RgBhWxvunpyQdeeYrj4BJELaJJ5yina421mJkHMRTwnYSbP+/93faZxhTIVe2vEAAAAldEVYdGRh
dGU6Y3JlYXRlADIwMjMtMTAtMTJUMTE6MjA6MzIrMDI6MDD7aUGnAAAAJXRFWHRkYXRlOm1vZGlm
eQAyMDIzLTEwLTEyVDExOjIwOjMyKzAyOjAwijT5GwAAAABJRU5ErkJggg==" />
</svg>
</div>


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

项目文档: [https://github.com/PyWebBuilders/bframe-docs](https://pywebbuilders.github.io/bframe-docs/)

项目DEMO: [https://github.com/PyWebBuilders/Plats.git](https://github.com/PyWebBuilders/Plats.git)
