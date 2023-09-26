"""
MIT License

Copyright (c) 2023 Bean-jun

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from bframe import request
from bframe import abort
from bframe.server import HTTP_METHOD


class View:
    method = HTTP_METHOD
    decorators = list()
    action = dict()
    notimpl_view = lambda *a, **kw: abort(404)

    def dispatch(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def as_view(cls, *class_args, **class_kwargs):

        def view(*args, **kwds):
            self = view.view_class(*class_args, **class_kwargs)
            return self.dispatch(*args, **kwds)

        if cls.decorators:
            # dispatch before
            for decorator in cls.decorators:
                view = decorator(view)

        view.view_class = cls
        view.__module__ = cls.__module__
        view.__doc__ = cls.__doc__
        view.method = cls.method    # 实现路由接口映射
        return view


class MethodView(View):

    def dispatch(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)

        if meth is None and request.method == "HEAD":
            meth = getattr(self, "get", self.notimpl_view)

        return meth(*args, **kwargs)
