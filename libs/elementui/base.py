import enum


class ElWidget:
    def __init__(self):
        pass


class ElPage(enum.Enum):
    TABLE = "table"
    FORM = "form"
    CUSTOM = "custom"

class ElApis:
    def __init__(self, list:str,create:str,update:str,delete:str,**kwargs):
        self.list = list
        self.create = create
        self.update = update
        self.delete = delete
        for key, value in kwargs.items():
            setattr(self, key, value)

class ElConfirm:
    def __init__(self, title:str, message:str, **kwargs):
        self.title = title
        self.message = message
        for key, value in kwargs.items():
            setattr(self, key, value)