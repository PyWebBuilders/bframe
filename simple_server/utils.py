def to_bytes(c):
    if isinstance(c, bytes):
        return c
    elif isinstance(c, str):
        return c.encode()
    else:
        return str(c).encode()