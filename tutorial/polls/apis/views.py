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

    def create(self):
        sess = self.get_session()
        body_kwargs = self.get_table_body_kwargs()
        body_kwargs["userid"] = session["userid"]
        obj = self.get_table(**body_kwargs)
        sess.add(obj)
        sess.query(Choice).filter_by(id=body_kwargs.get("choiceid")).update({Choice.votes: Choice.votes+1},
                                                                            synchronize_session='evaluate')
        sess.commit()
        return self.to_serializer(obj, 1)
