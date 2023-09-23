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
from bframe import request
from bframe.view import View
from bframe import abort


class GenericView(View):

    @classmethod
    def as_view(cls, action, *class_args, **class_kwargs):
        def view(*args, **kwds):
            self = view.view_class(*class_args, **class_kwargs)     #noqa
            self.action = action
            return self.dispatch(*args, **kwds)

        if cls.decorators:
            for decorator in cls.decorators:
                view = decorator(view)

        view.view_class = cls
        view.__module__ = cls.__module__
        view.__doc__ = cls.__doc__
        view.method = cls.method
        return view

    def dispatch(self, *args, **kwargs):
        action_str = self.action.get(request.method.lower())
        if action_str is None and request.method == "HEAD":
            action_str = self.action.get("get")

        meth = action_str and getattr(self, action_str) or self.notimpl_view

        return meth(*args, **kwargs)


class GenericAPIView(GenericView):

    table_class = None                          # 模型表
    table_class_primary_key = "id"              # 模型表主键
    table_serializer = None                     # 模型序列化类
    default_limit = 20                          # 默认查询总量
    default_limit_key = "_limit"                # 默认查询总量key
    default_offset = 1                          # 默认分页数
    default_offset_key = "_offset"              # 默认分页数key
    default_order_by = table_class_primary_key  # 数据查询排序字段
    default_order_by_key = "_order_by"          # 数据查询排序字段key
    default_order = "asc"                       # 数据查询排序字段顺序
    default_order_key = "_order"                # 数据查询排序字段顺序key

    @property
    def get_table(self):
        """获取数据模型"""
        if self.table_class is None:
            raise Exception(
                f"{self.__class__.__name__} not set table class"
            )
        return self.table_class

    @property
    def get_serializer(self):
        """获取数据模型序列化器"""
        if self.table_serializer is None:
            raise Exception(
                f"{self.__class__.__name__} not set table serizlizer"
            )
        return self.table_serializer

    def get_session(self):
        raise NotImplementedError

    def get_table_filter_kwargs(self):
        """获取请求过滤字段"""
        kw = dict()
        table = self.get_table
        for key, value in request.args.items():
            if hasattr(table, key):
                kw[key] = value
        return kw

    def get_table_body_kwargs(self):
        """获取请求体过滤字段"""
        kw = dict()
        table = self.get_table
        for key, value in request.forms.items():
            if hasattr(table, key):
                kw[key] = value
        return kw

    def get_table_filter_by_pk(self, pk, pk_key="pk"):
        table = self.get_table
        if not hasattr(table, pk_key):
            raise Exception(f"{table.__class__.__name__} not {pk_key} attr")
        return {pk_key: pk}

    def get_table_order_by_kwargs(self):
        """获取请求排序字段"""
        order_by = request.args.get(self.default_order_by_key,
                                    self.default_order_by)
        order = request.args.get(self.default_order_key,
                                 self.default_order)
        return {
            order_by: order
        }

    def get_table_limit_by_kwargs(self):
        """获取请求分页字段"""
        limit = request.args.get(self.default_limit_key,
                                 self.default_limit)
        offset = request.args.get(self.default_offset_key,
                                  self.default_offset)
        return int(limit), int(offset)

    def update_table_obj(self, obj, kwargs):
        for k, v in kwargs.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        return obj

    def make_condition(self, kwargs):
        condition = []
        table = self.get_table
        for k, v in kwargs.items():
            condition.append(getattr(table, k) == v)
        return condition

    def make_order(self, kwargs):
        orders = []
        table = self.get_table
        for k, v in kwargs.items():
            if hasattr(table, k):
                orders.append(getattr(getattr(table, k), v)())
        return orders

    def to_serializer(self, objs, count=0):
        serizlizer = self.get_serializer
        return serizlizer(objs, count).to_json()


class ListMixAPI:

    def list(self):
        table = self.get_table
        filter_kwargs = self.get_table_filter_kwargs()
        order_by_kwargs = self.get_table_order_by_kwargs()
        limit, offset = self.get_table_limit_by_kwargs()

        query = self.get_session().query(table).filter(*self.make_condition(filter_kwargs)).\
            order_by(*self.make_order(order_by_kwargs))
        count = query.count()
        objs = query.limit(limit).offset((offset-1)*limit).all()
        return self.to_serializer(objs, count)


class CreateMixAPI:

    def create(self):
        table = self.get_table
        session = self.get_session()
        body_kwargs = self.get_table_body_kwargs()
        obj = table(**body_kwargs)
        session.add(obj)
        session.commit()
        return self.to_serializer(obj, 1)


class RetrieveMixAPI:

    def retrieve(self, pk):
        table = self.get_table
        filter_kwargs = self.get_table_filter_by_pk(pk,
                                                    self.table_class_primary_key)
        query = self.get_session().query(table).filter(
            *self.make_condition(filter_kwargs))
        obj = query.first()
        if obj is None:
            return abort(404)
        count = query.count()
        return self.to_serializer(obj, count)


class UpdateMixAPI:

    def update(self, pk):
        table = self.get_table
        filter_kwargs = self.get_table_filter_by_pk(pk,
                                                    self.table_class_primary_key)
        session = self.get_session()
        obj = session.query(table).filter(
            *self.make_condition(filter_kwargs)).first()
        if obj is None:
            return abort(404)
        body_kwargs = self.get_table_body_kwargs()
        obj = self.update_table_obj(obj, body_kwargs)
        session.commit()
        return self.to_serializer(obj, 1)


class PatchMixAPI:

    def partial_update(self, pk):
        table = self.get_table
        filter_kwargs = self.get_table_filter_by_pk(pk,
                                                    self.table_class_primary_key)
        session = self.get_session()
        obj = session.query(table).filter(
            *self.make_condition(filter_kwargs)).first()
        if obj is None:
            return abort(404)
        body_kwargs = self.get_table_body_kwargs()
        obj = self.update_table_obj(obj, body_kwargs)
        session.commit()
        return self.to_serializer(obj, 1)


class DestroyMixAPI:

    def destroy(self, pk):
        table = self.get_table
        session = self.get_session()
        filter_kwargs = self.get_table_filter_by_pk(pk,
                                                    self.table_class_primary_key)
        query = self.get_session().query(table).filter(
            *self.make_condition(filter_kwargs))
        count = query.count()
        obj = query.first()
        if obj is None:
            return abort(404)
        session.delete(obj)
        session.commit()
        return self.to_serializer(obj, count)


class ListCreateAPI(GenericAPIView,
                    ListMixAPI,
                    CreateMixAPI):
    pass


class RetrieveUpdateAPI(GenericAPIView,
                        RetrieveMixAPI,
                        UpdateMixAPI):
    pass


class RetrieveDestroyAPI(GenericAPIView,
                         RetrieveMixAPI,
                         DestroyMixAPI):
    pass


class RetrieveUpdateDestroyAPI(GenericAPIView,
                               RetrieveMixAPI,
                               UpdateMixAPI,
                               DestroyMixAPI):
    pass


class RetrieveUpdatePatchDestroyAPI(GenericAPIView,
                                    RetrieveMixAPI,
                                    UpdateMixAPI,
                                    PatchMixAPI,
                                    DestroyMixAPI):
    pass


class ViewSet(GenericAPIView,
              ListMixAPI,
              CreateMixAPI,
              RetrieveMixAPI,
              UpdateMixAPI,
              PatchMixAPI,
              DestroyMixAPI):
    pass


class DefaultRouter:
    """路由支持"""

    def __init__(self, app):
        self.app = app
        pass

    def register(self, url: str, view_set: ViewSet):
        self.app.add_route(url, view_set.as_view({
            "get": "list",
            "post": "create",
        }))
        self.app.add_route(f"{url}/<int:pk>", view_set.as_view({
            "get": "retrieve",
            "post": "update",
            "put": "partial_update",
            "delete": "destroy",
        }))
