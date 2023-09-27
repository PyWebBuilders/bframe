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
