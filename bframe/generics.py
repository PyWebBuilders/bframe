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


class GenericView(View):

    @classmethod
    def as_view(cls, action, *class_args, **class_kwargs):
        def view(*args, **kwds):
            self = view.view_class(*class_args, **class_kwargs)
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

        if action_str is None:
            meth = self.notimpl_view
        else:
            meth = getattr(self, action_str, self.notimpl_view)

        return meth(*args, **kwargs)


class GenericAPIView(GenericView):
    pass

class ListMixAPI:

    def list(self):
        return "list"


class CreateMixAPI:

    def create(self):
        return "create"


class RetrieveMixAPI:

    def retrieve(self, pk):
        return f"retrieve pk={pk}"


class UpdateMixAPI:

    def update(self, pk):
        return f"update pk={pk}"


class PatchMixAPI:

    def partial_update(self, pk):
        return f"partial update pk={pk}"


class DestroyMixAPI:

    def destroy(self, pk):
        return f"destroy pk={pk}"


class ListCreateAPI(GenericAPIView,
                    ListMixAPI,
                    CreateMixAPI):
    pass


class RetrieveUpdateAPI(GenericAPIView,
                        RetrieveMixAPI,
                        UpdateMixAPI):
    pass


class RetrieveDestoryAPI(GenericAPIView,
                         RetrieveMixAPI,
                         DestroyMixAPI):
    pass


class RetrieveUpdateDestoryAPI(GenericAPIView,
                               RetrieveMixAPI,
                               UpdateMixAPI,
                               DestroyMixAPI):
    pass


class RetrieveUpdatePatchDestoryAPI(GenericAPIView,
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
