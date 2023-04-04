import datetime
import os
import typing as t
from http import HTTPStatus


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


class AbortExecept(Exception):
    pass


def abort(code: int, desc: str = ""):
    if desc == "" or not desc:
        desc = get_code_desc(code)
    raise AbortExecept(code, desc)


def parse_execept_code(e: Exception):
    if isinstance(e, AbortExecept):
        code = e.args[0]
    elif len(e.args) >= 2 and e.args[0].isdigit():
        code = e.args[0]
    else:
        code = 500
    return code
