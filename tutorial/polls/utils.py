from functools import wraps

from bframe import g, session

from models import Session, User


def login_decoroter(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        userid = session["userid"]
        if not userid:
            return "no login"
        user = Session.query(User).filter_by(id=userid).first()
        if not user:
            return "no login"
        g.user = user
        return f(*args, **kwargs)
    return wrapper
