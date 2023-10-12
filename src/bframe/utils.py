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
import datetime
import os
import typing as t
from http import HTTPStatus

from bframe._except import AbortExcept

RESPONSES_DICT = {
    v: (v.phrase, v.description)
    for v in HTTPStatus.__members__.values()
}


def now() -> datetime.datetime:
    return datetime.datetime.now()


def date2str(d: datetime.datetime, format="%Y-%m-%d %H:%M:%S") -> str:
    return d.strftime(format)


def str2date(t: str, format="%Y-%m-%d %H:%M:%S") -> datetime.datetime:
    return datetime.datetime.strptime(t, format)


def to_bytes(c: t.Any) -> bytes:
    if isinstance(c, bytes):
        return c
    elif isinstance(c, str):
        return c.encode()
    else:
        return str(c).encode()


def to_str(c: t.Any) -> str:
    if isinstance(c, bytes):
        return c.decode()
    elif isinstance(c, str):
        return c
    else:
        return str(c)


def resolve_filename_conflict(target_folder: str, basename: str) -> str:
    name, ext = os.path.splitext(basename)
    while True:
        newname = '%s_%s%s' % (name, date2str(now(), "%Y_%m_%d_%H_%M_%S"), ext)
        if not os.path.exists(os.path.join(target_folder, newname)):
            return newname


def archive_file(target_folder: str, filename: str, size: int = 5 << 20):
    filepath = os.path.join(target_folder, filename)
    if not os.path.exists(filepath):
        return
    if os.stat(filepath).st_size >= size:
        new_filename = resolve_filename_conflict(target_folder, filename)
        os.rename(filepath, new_filename)


def get_code_desc(code: int) -> str:
    return RESPONSES_DICT.get(code)[0]


def abort(code: int, desc: str = ""):
    try:
        if desc == "" or not desc:
            desc = get_code_desc(code)
    finally:
        raise AbortExcept(code, desc)


def parse_except_code(e: Exception):
    if isinstance(e, AbortExcept):
        code = e.args[0]
    elif len(e.args) >= 2 and e.args[0].isdigit():
        code = e.args[0]
    else:
        code = 500
    return code


class TEXT:
    BLACK = '\033[' + "30m"
    RED = '\033[' + "31m"
    GREEN = '\033[' + "32m"
    YELLOW = '\033[' + "33m"
    BLUE = '\033[' + "34m"
    MAGENTA = '\033[' + "35m"
    CYAN = '\033[' + "36m"
    WHITE = '\033[' + "37m"
    RESET = '\033[' + "39m"


class BACK:
    BLACK = '\033[' + "40m"
    RED = '\033[' + "41m"
    GREEN = '\033[' + "42m"
    YELLOW = '\033[' + "43m"
    BLUE = '\033[' + "44m"
    MAGENTA = '\033[' + "45m"
    CYAN = '\033[' + "46m"
    WHITE = '\033[' + "47m"
    RESET = '\033[' + "49m"


class STYLE:
    BRIGHT = '\033[' + "1m"
    NORMAL = '\033[' + "22m"
    RESET_ALL = '\033[' + "0m"


def color_msg(msg, color=TEXT.RED, back=BACK.BLACK, style=STYLE.NORMAL):
    return color + back + style + str(msg) + TEXT.RESET + BACK.RESET + STYLE.RESET_ALL
