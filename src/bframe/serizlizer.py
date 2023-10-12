
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
import datetime


class BaseSerializer:
    """
    序列化器
    """

    def __init__(self, *args, **kwargs):
        pass

    def to_json(self):
        raise NotImplementedError


class SimpleSerializer(BaseSerializer):
    """模型对象序列化器"""

    def __init__(self, objs, count=0):
        self.objs = objs if isinstance(objs, (tuple, list)) else [objs]
        self.count = count

    def to_dict(self, obj):
        dic = {}
        for column in obj.__table__.columns:
            dic[column.name] = getattr(obj, column.name)
        return dic

    def list_to_dict(self):
        list_dic = []
        for obj in self.objs:
            list_dic.append(self.to_dict(obj))
        return list_dic

    def to_json(self):
        return {
            "list": self.list_to_dict(),
            "count": self.count
        }


class DatetimeSerializer(SimpleSerializer):
    """日期时间序列化器"""

    def cure_value(self, value):
        if isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        if isinstance(value, datetime.datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return str(value)

    def to_dict(self, obj):
        dic = {}
        for column in obj.__table__.columns:
            value = getattr(obj, column.name)
            dic[column.name] = self.cure_value(value)
        return dic
