### 一、创建一个简单的app应用

1. 安装软件包

    ```python
    # 确保您已经安装python,在终端中输入此命令查看
    python -V
    # 安装本项目包
    python -m pip install bframe
    # 安装sqlalchemy包
    python -m pip install sqlalchemy
    ```

2. 编辑源码

    ```python
    # app.py
    from bframe import Frame


    app = Frame(__name__)


    @app.get("/ping")
    def pong():
        return "pong"


    if __name__ == "__main__":
        app.run()
    ```

3. 执行项目代码

    ```shell
    python app.py
    ```

4. 浏览器打开`http://localhost:7256/ping`查看


### 二、编写配置文件&数据库模型

1. 编辑配置文件

    ```python
    # config.py
    SQLALCHEMY_DATABASE_URI = "sqlite:///polls.db"
    ```

2. 编辑模型文件

    ```python
    # models.py
    import datetime

    from bframe import Frame
    from sqlalchemy import Column, DateTime, Integer, String, create_engine
    from sqlalchemy.engine.base import Engine
    from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

    Session: scoped_session = None
    engine: Engine = None


    def init_models(app: Frame):
        global Session, engine
        url = app.Config.get("SQLALCHEMY_DATABASE_URI")
        echo = app.Config.get("DEBUG")
        engine = create_engine(url, echo=echo)
        Session = scoped_session(sessionmaker(engine))


    Base = declarative_base()


    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True)
        username = Column(String(100), unique=True, nullable=False, comment="用户名")
        password = Column(String(100), nullable=False, comment="密码")
        createtime = Column(DateTime, default=datetime.datetime.now,
                            comment="创建时间")
        updatetime = Column(DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now, comment="修改时间")


    class Question(Base):
        __tablename__ = 'questions'

        id = Column(Integer, primary_key=True)
        content = Column(String(256), nullable=False, comment="问题")
        createtime = Column(DateTime, default=datetime.datetime.now,
                            comment="创建时间")
        updatetime = Column(DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now, comment="修改时间")


    class Choice(Base):
        __tablename__ = 'choices'

        id = Column(Integer, primary_key=True)
        question = Column(Integer, nullable=False, comment="问题id")
        content = Column(String(256), nullable=False, comment="结果")
        votes = Column(Integer, default=0, comment="投票数量")
        createtime = Column(DateTime, default=datetime.datetime.now,
                            comment="创建时间")
        updatetime = Column(DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now, comment="修改时间")


    class UserChoice(Base):
        __tablename__ = 'user_choices'

        id = Column(Integer, primary_key=True)
        choiceid = Column(Integer, nullable=False, comment="结果")
        userid = Column(Integer, nullable=False, comment="用户ID")
        createtime = Column(DateTime, default=datetime.datetime.now,
                            comment="创建时间")
        updatetime = Column(DateTime, default=datetime.datetime.now,
                            onupdate=datetime.datetime.now, comment="修改时间")


    def init_db(engine):
        Base.metadata.create_all(engine)
    ```

3. 改造app.py文件

    ```python
    from bframe import Frame


    def create_app(config):
        app = Frame(__name__)
        # 加载配置文件
        app.Config.from_py(config)

        # init sqlalchemy object
        from models import init_models
        init_models(app)

        # init db object
        from models import init_db, engine
        init_db(engine)

        @app.get("/ping")
        def pong():
            return "pong"
        return app


    app = create_app("config.py")

    if __name__ == "__main__":
        app.run()
    ```

4. 项目目录树

    ```shell
    .
    ├── app.py
    ├── config.py
    ├── models.py
    └── polls.db
    ```


### 三、视图的小试牛刀

1. 编辑视图文件

    ```python
    # 通过ViewSet快速实现接口的crud
    # view.py
    from bframe.generics import ViewSet
    from bframe.serizlizer import DatetimeSerializer
    from models import Choice, Question, Session, User, UserChoice


    class UserViewSet(ViewSet):
        table_class = User
        table_serializer = DatetimeSerializer

        def get_session(self):
            return Session


    class QuestionViewSet(ViewSet):
        table_class = Question
        table_serializer = DatetimeSerializer

        def get_session(self):
            return Session


    class ChoiceViewSet(ViewSet):
        table_class = Choice
        table_serializer = DatetimeSerializer

        def get_session(self):
            return Session


    class UserChoiceViewSet(ViewSet):
        table_class = UserChoice
        table_serializer = DatetimeSerializer

        def get_session(self):
            return Session
    ```

2. 改造app.py文件

    ```python
    from bframe import Frame


    def create_app(config):
        app = Frame(__name__)
        # 加载配置文件
        app.Config.from_py(config)

        # init sqlalchemy object
        from models import init_models
        init_models(app)

        # init db object
        from models import init_db, engine
        init_db(engine)

        # init apis
        from apis.views import UserViewSet, QuestionViewSet, ChoiceViewSet, UserChoiceViewSet
        from bframe.generics import DefaultRouter
        router = DefaultRouter(app)
        router.register("/users", UserViewSet)
        router.register("/questions", QuestionViewSet)
        router.register("/choices", ChoiceViewSet)
        router.register("/user_choices", UserChoiceViewSet)

        @app.get("/ping")
        def pong():
            return "pong"
        return app


    app = create_app("config.py")

    if __name__ == "__main__":
        app.run()
    ```

3. 目录树

    ```shell
    .
    ├── apis
    │   └── views.py
    ├── app.py
    ├── config.py
    ├── models.py
    └── polls.db
    ```

4. 通过curl查看接口

    ```shell
    # 创建用户
    curl http://localhost:7256/users -X POST -d "username=tom&password=tom"
    # 创建问题
    curl http://localhost:7256/questions -X POST -d "content=你喜欢下雨天气么？"
    # 获取问题
    curl http://localhost:7256/questions
    # 创建问题答案
    curl http://localhost:7256/choices -X POST -d "question=1&content=喜欢"
    curl http://localhost:7256/choices -X POST -d "question=1&content=不喜欢"
    # 获取问题答案
    curl http://localhost:7256/choices
    # 创建投票
    curl http://localhost:7256/user_choices -X POST -d "userid=1&choiceid=1"
    # 查询投票
    curl http://localhost:7256/user_choices
    ```

### 四、添加用户认证功能，让投票更具备真实性

1. 实现登录装饰器

    ```python
    # utils.py
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
    ```

2. 为通用类视图添加装饰器

    ```python
    class UserViewSet(ViewSet):
        table_class = User
        table_serializer = DatetimeSerializer
        decorators = [login_decoroter]

        def get_session(self):
            return Session


    class QuestionViewSet(ViewSet):
        table_class = Question
        table_serializer = DatetimeSerializer
        decorators = [login_decoroter]

        def get_session(self):
            return Session


    class ChoiceViewSet(ViewSet):
        table_class = Choice
        table_serializer = DatetimeSerializer
        decorators = [login_decoroter]

        def get_session(self):
            return Session


    class UserChoiceViewSet(ViewSet):
        table_class = UserChoice
        table_serializer = DatetimeSerializer
        decorators = [login_decoroter]

        def get_session(self):
            return Session
    ```

3. 编辑用户注册视图

    ```python
    # apis/views.py
    import base64

    from bframe import MethodView, request, session
    from bframe.generics import ViewSet
    from bframe.serizlizer import DatetimeSerializer
    from models import Choice, Question, Session, User, UserChoice
    from utils import login_decoroter


    class RegisterView(MethodView):

        def post(self):
            """
            用户注册
            """
            username = request.forms.get("username")
            password = request.forms.get("password")
            if not all([username, password]):
                return {
                    "status": False,
                    "msg": "参数缺失"
                }
            user = Session.query(User).filter_by(username=username).first()
            if user:
                return {
                    "status": False,
                    "msg": "用户已注册"
                }

            # base64编码密码不安全，请使用更安全的方式保存密码
            user = User(username=username,
                        password=base64.b64encode(password.encode()).decode())
            Session.add(user)
            Session.commit()
            session["userid"] = user.id
            return {
                "status": True,
                "msg": "登录成功"
            }
    ```

4. 编辑用户登录视图

    ```python
    # apis/views.py
    import base64

    from bframe import MethodView, request, session
    from bframe.generics import ViewSet
    from bframe.serizlizer import DatetimeSerializer
    from models import Choice, Question, Session, User, UserChoice
    from utils import login_decoroter


    class LoginView(MethodView):

        def post(self):
            """
            用户登录
            """
            username = request.forms.get("username")
            password = request.forms.get("password")
            if not all([username, password]):
                return {
                    "status": False,
                    "msg": "参数缺失"
                }
            user = Session.query(User).filter_by(username=username).first()
            if not user:
                return {
                    "status": False,
                    "msg": "用户不存在"
                }

            # base64编码密码不安全，请使用更安全的方式保存密码
            if user.password != base64.b64encode(password.encode()).decode():
                return {
                    "status": False,
                    "msg": "账号或密码异常"
                }
            session["userid"] = user.id
            return {
                "status": True,
                "msg": "登录成功"
            }
    ```

5. 更新app.py,注册视图,移除部分视图

    ```python
    from bframe import Frame


    def create_app(config):
        app = Frame(__name__)
        # 加载配置文件
        app.Config.from_py(config)

        # init sqlalchemy object
        from models import init_models
        init_models(app)

        # init db object
        from models import init_db, engine
        init_db(engine)

        # init apis
        from apis.views import RegisterView, LoginView, UserViewSet, QuestionViewSet, ChoiceViewSet, UserChoiceViewSet
        from bframe.generics import DefaultRouter
        app.add_route("/register", RegisterView.as_view())
        app.add_route("/login", LoginView.as_view())
        router = DefaultRouter(app)
        # router.register("/users", UserViewSet)
        router.register("/questions", QuestionViewSet)
        router.register("/choices", ChoiceViewSet)
        router.register("/user_choices", UserChoiceViewSet)

        @app.get("/ping")
        def pong():
            return "pong"
        return app


    app = create_app("config.py")

    if __name__ == "__main__":
        app.run()
    ```


### 五、编辑前端页面，接上咱们开发的接口





