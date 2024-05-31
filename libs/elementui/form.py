from libs.elementui.base import ElWidget


class ElFormItem(ElWidget):
    def __init__(self, label: str, prop: str, type: str = "input", props: dict = {}, **kwargs):
        self.label = label
        self.prop = prop
        self.type = type
        self.props = props
        for key, value in kwargs.items():
            setattr(self, key, value)


class ElInput(ElFormItem):
    def __init__(self, label: str, prop: str, **kwargs):
        super().__init__(label, prop, "input", {}, **kwargs)


class ElNumberInput(ElFormItem):
    def __init__(self, label: str, prop: str, **kwargs):
        super().__init__(label, prop, "input", {"type": "number"}, **kwargs)


class ElForm(ElWidget):
    def __init__(
        self,
        title: str,
        rows: list[list[ElFormItem]] = [],
        submit_api: str = "",
        **kwargs,
    ):
        self.title = title
        self.rows = rows
        self.submit_api = submit_api
