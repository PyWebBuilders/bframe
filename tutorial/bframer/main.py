import sqlite3

from bframe import Frame, Redirect, abort, request

app = Frame(__name__, static_url="", static_folder="static")
conn = sqlite3.connect("bframer.db")


def dict_factory(cur, row):
    dic = {}
    for idx, col in enumerate(cur.description):
        dic[col[0]] = row[idx]
    return dic


conn.row_factory = dict_factory
cur = conn.cursor(sqlite3.Cursor)

defualt_account = "admin"
defualt_password = "admin"
create_sql = """
create table article (
    id INTEGER  primary key autoincrement,
    title varchar(100) not null,
    content text
);
"""
find_table_sql = "select * from sqlite_master where type='table' and name in ('user', 'article')"


def init_db():
    ret = cur.execute(find_table_sql).fetchall()
    if len(ret) > 0:
        print("init db sucessful~")
        return
    cur.executescript(create_sql)


def returnJson(code, msg, data):
    return {
        "code": code,
        "message": msg,
        "data": data
    }


def returnOk(data):
    return returnJson(200, "ok", data)


def returnFailed(data=None):
    return returnJson(-1, "failed", data)


@app.get("/")
def index():
    return Redirect("/index.html")


@app.route("/api/<reg:(?P<version>v\d+$)>/home", method=["GET", "POST"])
def home(version):
    if version == "v1" and request.method == "GET":
        article = cur.execute("select * from article").fetchall()
        return returnOk(article)
    if version == "v1" and request.method == "POST":
        sql = """insert into article (title, content) values (\"%s\", \"%s\")"""
        cur.execute(sql % (request.forms.get("title"),
                    request.forms.get("content")))
        conn.commit()
        article = cur.execute("select * from article order by id desc limit 1").\
            fetchall()
        # return returnOk(article)
        return Redirect("/index.html")
    return abort(404)


@app.route("/api/<reg:(?P<version>v\d+$)>/login", method=["POST"])
def login(version):
    if version == "v1" and request.method == "POST":
        if request.forms.get("email") == defualt_account and request.forms.get("password") == defualt_password:
            return returnOk("")
        return returnFailed("login failed")
    return abort(404)


if __name__ == "__main__":
    try:
        init_db()
        app.run()
    except Exception as e:
        pass
    finally:
        conn.close()
