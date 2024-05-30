import enum
from libs.elementui.base import ElConfirm, ElWidget
from libs.elementui.form import ElForm


class ElTableColumn(ElWidget):
    def __init__(self, prop: str, label: str, type: str, props: dict, **kwargs):
        self.prop = prop
        self.label = label
        self.type = type
        self.props = props
        for key, value in kwargs.items():
            setattr(self, key, value)


class ElTableActionType(enum.Enum):
    FORM = "form"
    API = "api"
    ROUTER = "router"


class ElTableAction(object):
    def __init__(
        self,
        label: str,
        form_key: str,
        icon: str,
        api: str,
        path: str = "",
        params: dict = {},
        confirm:ElConfirm = ElConfirm("提示", "确定要修改吗？"),
        type: ElTableActionType = ElTableActionType.FORM,
    ):
        self.label = label
        self.icon = icon
        #form
        self.form_key = form_key  # 打开一个表单，form_key是表单的key，传入row
        #api
        self.api = api
        self.params = params
        #router
        self.path = path
        # universal 
        self.confirm = confirm
        self.type = type

class ElTableBatchAction(ElTableAction):
    def __init__(
        self,
        *args,
        row_id: str = "id",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.row_id = row_id
        


class ElTable(ElWidget):
    def __init__(
        self,
        title: str,
        columns: list[ElTableColumn] = [],
        search: ElForm = ElForm("Search"),
        filters: ElForm = ElForm("Filters"),
    ):
        self.title = title
        self.columns = columns
        self.search = search
        self.filters = filters
