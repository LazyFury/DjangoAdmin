from django.http import HttpRequest

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
                    ElMenuItem(
                        title="用户列表",
                        key="user-list",
                        path="/user/user-list",
                        component="TableView",
                        table=ElTable(
                            title="用户列表",
                            columns=[
                                ElTableColumn(
                                    prop="username",
                                    label="用户名",
                                    width="180",
                                    fixed="left",
                                )
                            ],
                        ),
                    ),
                ],
            ),
        ]
    )

