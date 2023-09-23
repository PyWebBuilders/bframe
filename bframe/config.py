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
import importlib
from collections import UserDict


DEFAULT_CONFIG = {
    # SESSION CONFIG
    "SESSION_ID": "_session",
    "SESSION_MAX_AGE": 604800,  # a week
    "SESSION_EXPIRES": None,
    "SESSION_PATH": "/",
    "SESSION_DOMAIN": None,
    "SESSION_SECURE": False,
    "SESSION_HTTPONLY": True,
    "SESSION_SAMESITE": None,
}


class BaseConfig(UserDict):

    def __init__(self, dict=None, /, **kwargs):
        super().__init__(dict, **kwargs)
        self.__initialize_default_config(DEFAULT_CONFIG)

    def __initialize_default_config(self, kwargs: dict):
        for key, value in kwargs.items():
            self.data[key] = value


class Config(BaseConfig):

    def from_py(self, path: str):
        if path.endswith(".py"):
            path = path.rstrip(".py")
        module = importlib.import_module(path)
        for attr in module.__dict__:
            if not attr.isupper():
                continue
            self.data[attr] = module.__dict__.get(attr)
