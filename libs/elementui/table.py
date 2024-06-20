import enum
from libs.elementui.base import ElConfirm, ElWidget
from libs.elementui.form import ElForm


class ElTableColumn(ElWidget):
    def __init__(
        self, prop: str, label: str, type: str = "", props: dict = {}, **kwargs
    ):
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
        api_key: str,
        path: str = "",
        param_keys: list[dict[str,str]] = [],
        confirm: ElConfirm | None = None,
        type: ElTableActionType = ElTableActionType.FORM,
        props: dict = {},
    ):
        self.label = label
        self.icon = icon
        # form
        self.form_key = form_key  # 打开一个表单，form_key是表单的key，传入row
        # api
        self.api_key = api_key
        self.param_keys = param_keys
        # router
        self.path = path
        # universal
        self.confirm = confirm
        self.type = type
        self.props = props


class ElTableBatchAction(ElTableAction):
    def __init__(
        self,
        *args,
        row_key: str = "",
        ids_name: str = "",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.row_key = row_key
        self.ids_name = ids_name


class DefActions:
    EDIT = ElTableAction(
        label="编辑",
        form_key="update|create",
        icon="ant-design:edit-outlined",
        api_key="update",
        type=ElTableActionType.FORM,
    )
    DELETE = ElTableAction(
        label="删除",
        form_key="",
        icon="ant-design:delete-outlined",
        api_key="delete",
        confirm=ElConfirm("提示", "确定要删除吗？", type="warning"),
        type=ElTableActionType.API,
        param_keys=[{"id":"id"}],
        props={
            "type": "danger",
        },
    )


class ElTable(ElWidget):
    def __init__(
        self,
        title: str,
        description:str="",
        columns: list[ElTableColumn] = [],
        search: ElForm = ElForm("Search"),
        filters: ElForm = ElForm("Filters"),
        actions: list[ElTableAction] = [
            DefActions.EDIT,
            DefActions.DELETE,
        ],
        batch_actions: list[ElTableBatchAction] = [
            ElTableBatchAction(
                label="批量删除",
                form_key="",
                icon="ant-design:delete-outlined",
                api_key="delete",
                confirm=ElConfirm("提示", "确定要删除吗？", type="warning"),
                type=ElTableActionType.API,
                row_key="id",
                ids_name="ids",
                props={
                    "type": "danger",
                },
            ),
        ],
        **kwargs,
    ):
        self.title = title
        self.columns = columns
        self.description = description
        self.search = search
        self.filters = filters
        self.actions = actions
        self.batch_actions = batch_actions
        for key, value in kwargs.items():
            setattr(self, key, value)
