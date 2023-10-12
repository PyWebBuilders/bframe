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
from bframe.wrappers import Request


class TestClient:

    def __init__(self, app) -> None:
        self.app = app

    def handle(self, method, url, data=None, headers=None):
        r = Request(method, url, headers=headers)
        r.Data = data if data else {}
        return self.app(r)

    def get(self, url, headers=None):
        return self.handle("GET", url, headers=headers)

    def post(self, url, data, headers=None):
        return self.handle("POST", url, data, headers=headers)

    def put(self, url, data, headers=None):
        return self.handle("PUT", url, data, headers=headers)

    def delete(self, url, data, headers=None):
        return self.handle("DELETE", url, data, headers=headers)
