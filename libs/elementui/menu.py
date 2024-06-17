from typing import Self

from common.wrapped import jsonGetter
from libs.elementui.base import ElApis, ElPage, ElWidget
from libs.elementui.form import ElForm
from libs.elementui.table import ElTable


class ElMenuGap (ElWidget):
    def __init__(self,title=""):
        self.type = "gap"
        self.title = title

class ElMenuItem(ElWidget):
    def __init__(
        self,
        title: str,
        key: str,
        path: str,
        component: str,
        icon: str = "",
        children: list[Self|ElMenuGap] = [],
        table:ElTable = ElTable(""),
        api:ElApis = ElApis("","","",""),
        forms:dict[str,ElForm] = {
            "create": ElForm("Create"),
            "update": ElForm("Update"),
        },
        type=ElPage.TABLE,
    ):
        self.type = "menu-item"
        self.title = title
        self.key = key
        self.icon = icon
        self.path = path
        self.component = component
        self.children = children
        self.table = table
        self.api = api
        self.forms = forms
        self.type = type

    @jsonGetter(name="title_lower")
    def title_lower(self):
        return self.title.lower()


class ElMenu(list):
    def __init__(self,children: list[ElMenuItem|ElMenuGap] = []):
        super().__init__(children)
