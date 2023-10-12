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
import json
import re
import typing as t
from http import cookies
from urllib.parse import unquote

from bframe.utils import to_bytes, to_str


class Cookie(cookies.SimpleCookie):

    def output(self, attrs=None, header="Set-Cookie:", sep="\r\n") -> str:
        items = sorted(self.items())
        for key, value in items:
            yield value.OutputString(attrs)


class BaseFile:
    name: str = ""
    filename: str = ""
    file_type: str = ""
    body: bytes = b""

    def __init__(self,
                 name: str,
                 filename: str,
                 file_type: str,
                 body: bytes):
        self.name = name
        self.filename = filename
        self.file_type = file_type
        self.body = body

    def save(self, dst):
        with open(dst, "wb") as f:
            f.write(self.body)


class BaseRequest:
    Method: str = ""
    Path: str = ""
    Full_Path: str = ""
    Args: dict = {}
    Protoc: str = ""
    Headers: dict = {}
    Body: t.Union[str, bytes] = b""
    Data: dict = {}
    File: t.Dict[str, BaseFile] = {}
    Path_Args: dict = {}
    Cookies: Cookie = None

    def __init__(self,
                 method: str = "",
                 path: str = "",
                 protoc: str = "",
                 headers: dict = None):
        self.__initialize_args()
        self.Method = method
        self.Full_Path = path
        if "?" in path:
            self.Path, self.Args = BaseRequest.__initialize_path(path)
        else:
            self.Path = path
        self.Protoc = protoc
        if headers is None:
            headers = dict()
        self.Headers = {k.replace("_", "-").title(): v
                        for k, v in headers.items()}
        if "Cookie" in self.Headers:
            self.Cookies.load(self.Headers.get("Cookie"))

    def __initialize_args(self):
        """初始化参数,避免地址引用导致数据异常"""
        self.Method = ""
        self.Path = ""
        self.Args = {}
        self.Protoc = ""
        self.Headers = {}
        self.Body = ""
        self.Data = {}
        self.File = {}
        self.Path_Args = {}
        self.Cookies = Cookie()

    @staticmethod
    def __initialize_path(path):
        path, args_str = path.split("?")
        args = dict()

        if args_str == "":
            return path, args
        for kv_item in args_str.split("&"):
            item = kv_item.split("=")
            if len(item) == 1:
                args.update({unquote(item[0]): None})
                continue
            args.update({unquote(item[0]): unquote(item[1])})
        return path, args

    def __parse_form_data(self):
        disposition = b"Content-Disposition: form-data; "

        def get_boundary(content_type):
            return content_type[len("multipart/form-data; boundary="):]

        def is_package(body):
            if b"content-type" in body or b"Content-Type" in body:
                return True
            return False

        def get_filed_name(line):
            ret = re.match(disposition + b'name="(.+)"', line)
            return ret.groups()[0]

        def get_file_filed_name(line):
            ret = re.match(disposition + b'name="(.+)"; filename="(.+)"', line)
            return ret.groups()

        content_type = self.Headers.get("Content-Type")
        boundary = get_boundary(content_type)

        lines = self.Body.split(to_bytes(boundary))
        for line in lines:
            if not line.startswith(b"\r\n"):
                continue
            line_list = line.split(b"\r\n")
            if len(line_list) >= 5 and is_package(line):
                name, filename, filetype, body = "", "", "", b""
                type_status = False
                name_status = False
                for __line in line_list:
                    if __line.startswith((b"Content-Type", b"content-type")):
                        filetype = __line[len("Content-Type: "):]
                        type_status = True
                        continue
                    if __line.startswith((b"Content-Disposition: form-data;")):
                        name, filename = get_file_filed_name(__line)
                        name_status = True
                        continue
                    if type_status and name_status:
                        break
                body = b"\r\n".join(line_list[4:len(line_list) - 1])
                self.File[to_str(name)] = BaseFile(
                    to_str(name),
                    to_str(filename),
                    to_str(filetype),
                    body)
            else:
                __name = get_filed_name(line_list[1])
                __value = line_list[3]
                self.Data.update({unquote(to_str(__name)): unquote(to_str(__value))})  # noqa

    def __parse_form_urlencoded(self):
        for kv_entitry in self.Body.split(b"&"):
            kv_split = kv_entitry.split(b"=")
            filed, value = kv_split[0], b""
            if len(kv_split) == 2:
                value = kv_split[1]
            self.Data.update({unquote(to_str(filed)): unquote(to_str(value))})

    def __parse_json(self):
        self.Data.update(json.loads(self.Body))

    def parse_body(self, data):
        self.Body = data
        if not self.Body or self.Headers.get("Content-Length") in [0, "0"]:
            return
        content_type = self.Headers.get("Content-Type")

        if content_type.startswith("multipart/form-data"):
            return self.__parse_form_data()
        elif content_type.startswith("application/x-www-form-urlencoded"):
            return self.__parse_form_urlencoded()
        elif content_type.startswith("application/json"):
            return self.__parse_json()
        # TODO: parse other type
        ...

    def set_path_args(self, **kwds):
        self.Path_Args.update(kwds)


class Request(BaseRequest):

    @property
    def forms(self):
        return self.Data

    @property
    def args(self):
        return self.Args

    @property
    def files(self):
        return self.File

    @property
    def method(self):
        return self.Method

    @property
    def path(self):
        return self.Path

    @property
    def full_path(self):
        return self.Full_Path

    @property
    def headers(self):
        return self.Headers


class Response:
    Code: int = 200
    Headers: dict = {}
    Body: str = ""
    Cookies: Cookie = None

    def __init__(self, code: int = 200, headers: dict = None, body: t.Union[str, bytes] = ""):
        self.Code = code
        self.Headers = headers if headers else dict()
        self.Body = body
        self.Cookies = Cookie()

    def set_cookies(self,
                    key,
                    value='',
                    max_age=None,
                    expires=None,
                    path='/',
                    domain=None,
                    secure=False,
                    httponly=False,
                    samesite=None):
        """
        set response cookie
        """
        self.Cookies[key] = value
        self.Cookies[key].update({
            "path": path,
            "secure": secure,
            "httponly": httponly,
        })

        if max_age:
            self.Cookies[key].update({"max-age": max_age})
        if expires:
            self.Cookies[key].update({"expires": expires})
        if domain:
            self.Cookies[key].update({"domain": domain})
        if samesite:
            self.Cookies[key].update({"samesite": samesite})


class Redirect(Response):

    def __init__(self, url: str):
        super().__init__(301, {"Location": url}, "")


def make_response(body):
    """
    params: body # Response body
    return: a Response object
    """
    if isinstance(body, (str, bytes)):
        body = to_bytes(body)
    if isinstance(body, dict):
        body = to_bytes(json.dumps(body))

    return Response(body=body)
