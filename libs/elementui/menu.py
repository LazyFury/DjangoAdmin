from typing import Self

from common.wrapped import jsonGetter
from libs.elementui.base import ElApis, ElPage, ElWidget
from libs.elementui.form import ElForm
from libs.elementui.table import ElTable


class ElMenuGap (ElWidget):
    def __init__(self,title="",icon=""):
        self.type = "gap"
        self.title = title
        self.icon = icon or "ant-design:align-left-outlined"

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
        hidden=False,
        currentForm:str = "create",
    ):
        self.type = "menu-item"
        self.title = title
        self.key = key
        self.icon = icon or "ant-design:file-text-outlined"
        self.path = path
        self.component = component
        self.children = children
        self.table = table
        self.api = api
        self.forms = forms
        self.type = type
        self.hidden = hidden
        self.currentForm = currentForm

    @jsonGetter(name="title_lower")
    def title_lower(self):
        return self.title.lower()


class ElMenu(list):
    def __init__(self,children: list[ElMenuItem|ElMenuGap] = []):
        super().__init__(children)
