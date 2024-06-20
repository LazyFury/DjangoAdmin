from libs.elementui.base import ElWidget


class ElFormItem(ElWidget):
    def __init__(self, label: str, prop: str, type: str = "input", props: dict = {},required=True, **kwargs):
        self.label = label
        self.prop = prop
        self.type = type
        self.props = props
        self.required = required
        for key, value in kwargs.items():
            setattr(self, key, value)


class ElInput(ElFormItem):
    def __init__(self, label: str, prop: str, **kwargs):
        super().__init__(label, prop, "input", {}, **kwargs)


class ElNumberInput(ElFormItem):
    def __init__(self, label: str, prop: str, **kwargs):
        super().__init__(label, prop, "input", {"type": "number"}, **kwargs)

class ElFormGap(ElFormItem):
    def __init__(self, **kwargs):
        super().__init__("", "", "gap", {}, **kwargs)

class ElFormTitle(ElFormItem):
    def __init__(self,lebel="", **kwargs):
        super().__init__(lebel, "", "title", {}, **kwargs)

class ElForm(ElWidget):
    def __init__(
        self,
        title: str,
        rows: list[list[ElFormItem]|ElFormGap|ElFormTitle] = [],
        submit_api: str = "",
        submit_api_key: str = "",
        detail_api: str = "",
        buttons_container_class_name: str = "",
        detail_param_keys: list[str] = [],
        **kwargs,
    ):
        self.title = title
        self.rows = rows
        self.submit_api = submit_api
        self.submit_api_key = submit_api_key
        self.detail_api = detail_api
        self.detail_param_keys = detail_param_keys
        self.buttons_container_class_name = buttons_container_class_name
        for key, value in kwargs.items():
            setattr(self, key, value)
