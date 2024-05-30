from django.http import HttpRequest

from common import serizalize
from common.response import ApiJsonResponse
from libs.elementui.menu import ElMenu, ElMenuItem
from . import api


@api.get("/menus")
def menus(request: HttpRequest):
    return ApiJsonResponse.success((ElMenu([
        ElMenuItem(
            title="Dashboard",
            key="dashboard",
            icon="el-icon-s-home",
            path="/dashboard",
            component="dashboard",
            children=[
                ElMenuItem(
                    title="Analysis",
                    key="analysis",
                    icon="el-icon-s-data",
                    path="/analysis",
                    component="analysis",
                ),
                ElMenuItem(
                    title="Monitor",
                    key="monitor",
                    icon="el-icon-s-operation",
                    path="/monitor",
                    component="monitor",
                ),
                ElMenuItem(
                    title="Workplace",
                    key="workplace",
                    icon="el-icon-s-platform",
                    path="/workplace",
                    component="workplace",
                ),
            ]
        )
    ])))
