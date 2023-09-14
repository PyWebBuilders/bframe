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
from urllib.parse import unquote

from bframe.utils import to_bytes, to_str


class BaseFile:

    name: str = ""
    filename: str = ""
    file_type: str = ""
    body: bytes = b""

    def __init__(self, name: str, filename: str, file_type: str, body: bytes) -> None:
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
    Args: dict = {}
    Protoc: str = ""
    Headers: dict = {}
    Body: str = b""
    Data: dict = {}
    File: dict[str:BaseFile] = {}

    def __init__(self, method: str = "", path: str = "", protoc: str = "", headers: dict = None):
        self.Method = method
        if "?" in path:
            self.Path, self.Args = self.__initializa_path(path)
        else:
            self.Path = path
        self.Protoc = protoc
        if headers is None:
            headers = dict()
        self.Headers = {k.replace("_", "-").lower(): v for k, v in headers.items()}

    def __initializa_path(self, path):
        path, args_str = path.split("?")
        args = dict()

        if args_str == "":
            return path, args
        for kv_item in args_str.split("&"):
            item = kv_item.split("=")
            args.update({unquote(item[0]): unquote(item[1])})
        return path, args

    def __parse_form_data(self):
        def get_boundary(content_type):
            return content_type[len("multipart/form-data; boundary="):]

        def is_package(body):
            if b"content-type" in body or b"Content-Type" in body:
                return True
            return False

        def get_filed_name(line):
            ret = re.match(b'Content-Disposition: form-data; name="(.+)"',
                           line)
            return ret.groups()[0]

        def get_file_filed_name(line):
            ret = re.match(b'Content-Disposition: form-data; name="(.+)"; filename="(.+)"',
                           line)
            return ret.groups()

        content_type = self.Headers.get("content-type")
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
                body = b"\r\n".join(line_list[4:len(line_list)-1])
                self.File[to_str(name)] = BaseFile(
                    to_str(name),
                    to_str(filename),
                    to_str(filetype),
                    body)
            else:
                __name = get_filed_name(line_list[1])
                __value = line_list[3]
                self.Data.update({to_str(__name): to_str(__value)})

    def __parse_form_urlencoded(self):
        for kv_entitry in self.Body.split(b"&"):
            kv_split = kv_entitry.split(b"=")
            filed, value = kv_split[0], b""
            if len(kv_split) == 2:
                value = kv_split[1]
            self.Data.update({to_str(filed): to_str(value)})

    def __parse_json(self):
        self.Data.update(json.loads(self.Body))

    def __parse_body(self, data):
        self.Body = data
        content_type = self.Headers.get("content-type")

        if content_type.startswith("multipart/form-data"):
            return self.__parse_form_data()
        elif content_type.startswith("application/x-www-form-urlencoded"):
            return self.__parse_form_urlencoded()
        elif content_type.startswith("application/json"):
            return self.__parse_json()
        # TODO: parse other type
        ...


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
    def headers(self):
        return self.Headers


class Response:

    Code: int = 200
    Headers: dict = {}
    Body: str = ""

    def __init__(self, code: int = 200, headers: dict = None, body: str = "") -> None:
        self.Code = code
        self.Headers = headers if headers else dict()
        self.Body = body


class Redirect(Response):

    def __init__(self, url: str):
        super().__init__(301, {"Location": url}, "")
