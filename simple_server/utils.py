import os
import datetime
import typing as t


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


def archive_file(target_folder: str, filename: str, size: int = 5 << 10):
    filepath = os.path.join(target_folder, filename)
    if os.stat(filepath).st_size >= size:
        new_filename = resolve_filename_conflict(target_folder, filename)
        os.rename(filepath, new_filename)
