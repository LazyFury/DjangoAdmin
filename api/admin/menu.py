from django.http import HttpRequest

from libs.elementui.base import ElApis
from libs.elementui.form import ElForm, ElFormItem
from libs.elementui.menu import ElMenu, ElMenuItem
from libs.elementui.table import ElTable, ElTableColumn
from . import api


@api.get("/menus")
def menus(request: HttpRequest):
    return ElMenu(
        [
            ElMenuItem(
                title="Dashboard",
                key="overview",
                icon="ant-design:dashboard-outlined",
                path="/overview",
                component="HomeView",
            ),
            ElMenuItem(
                title="用户管理",
                key="user",
                icon="ant-design:user-outline",
                path="/user",
                component="user",
                children=[
                    user_menu(),
                    user_group_menu(),
                    user_token_menu()
                ],
            ),
        ]
    )

def user_token_menu():
    return ElMenuItem(
        title="用户登录日志",
        key="user-log",
        path="/user/user-log",
        component="TableView",
        api=ElApis(list="/user-log.list")
    )


def user_menu():
    return ElMenuItem(
        title="用户列表",
        key="user-list",
        path="/user/user-list",
        component="TableView",
        table=ElTable(
            title="用户列表",
            columns=[
                ElTableColumn(prop="username", label="用户名", width="180"),
                ElTableColumn(
                    prop="email",
                    label="邮箱",
                    width="180",
                    type="link",
                    url_prefix="mailto:",
                ),
                ElTableColumn(prop="is_active", label="is_active", type="checkbox"),
            ],
        ),
        api=ElApis(
            list="/user.list",
            delete="/user.delete",
        ),
    )


def user_group_menu():
    return ElMenuItem(
        title="用户组",
        key="user-group",
        path="/user/user-group",
        component="TableView",
        table=ElTable(
            title="用户组",
            columns=[
                ElTableColumn(prop="name", label="名称", width="180"),
            ],
            search=ElForm(
                title="search",
                rows=[
                    [
                        ElFormItem(
                            label="用户组名称",
                            prop="name",
                            placeholder="请输入用户名",
                        ),
                        ElFormItem(
                            label="用户组名称",
                            prop="name",
                            placeholder="请输入用户名",
                        ),
                    ]
                ],
            ),
        ),
        api=ElApis(
            list="/user-group.list",
            delete="/user-group.delete",
            create="/user-group.create",
            update="/user-group.update",
        ),
        forms={
            "create": ElForm(
                title="创建用户组",
                rows=[
                    [
                        ElFormItem(
                            label="名称",
                            prop="name",
                            type="input",
                            placeholder="请输入",
                        )
                    ]
                ],
            ),
        },
    )
