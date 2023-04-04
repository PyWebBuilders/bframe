from threading import get_ident


class Local():

    def __init__(self):
        super().__setattr__("storage", {})

    def __setattr__(self, name, value):
        id = get_ident()
        if id in self.storage:
            self.storage[id][name] = value
        else:
            self.storage[id] = {name: value}

    def __getattr__(self, name):
        id = get_ident()
        return self.storage[id][name]


class LocalProxy():

    def __init__(self, local, name) -> None:
        self.__local = local
        self.__name = name

    def __getattr__(self, name):
        obj = getattr(self.__local, self.__name)
        return getattr(obj, name)
    
    def push(self, value):
        setattr(self.__local, self.__name, value)