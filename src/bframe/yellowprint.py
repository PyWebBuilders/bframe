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
from typing import Callable
from bframe.scaffold import MethodSenquenceAlias, Scaffold


class YellowPrint(Scaffold):

    def __init__(self,
                 yellowname: str,
                 name: str = None,
                 static_url="static",
                 static_folder="static",
                 url_prefix=None):
        super().__init__(name, static_url, static_folder)
        self.yellowname = yellowname
        self.url_prefix = url_prefix
        if url_prefix is None:
            self.url_prefix = f"/{self.yellowname}"

    def add_route(self,
                  url: str,
                  func_or_class: Callable,
                  method: MethodSenquenceAlias = None):
        if self.url_prefix:
            url = f"{self.url_prefix}{url}"
        super().add_route(url, func_or_class, method)

    def add_before_app_handle(self, f):
        self.before_funs_dict.setdefault(self.yellowname, []).append(f)
        return f

    def add_after_app_handle(self, f):
        self.after_funs_dict.setdefault(self.yellowname, []).append(f)
        return f
