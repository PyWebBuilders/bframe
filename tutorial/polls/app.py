from bframe import Frame
from bframe import Redirect


def create_app(config):
    app = Frame(__name__, static_url="")
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
    
    @app.get("/")
    @app.get("/index")
    def index():
        return Redirect("/index.html")

    return app


app = create_app("config.py")

if __name__ == "__main__":
    app.run()
