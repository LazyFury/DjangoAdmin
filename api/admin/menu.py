from turtle import width
from django.http import HttpRequest
from numpy import sort

from app import settings
from libs.elementui.base import ElApis
from libs.elementui.form import ElForm, ElFormItem
from libs.elementui.menu import ElMenu, ElMenuItem
from libs.elementui.table import (
    DefActions,
    ElTable,
    ElTableAction,
    ElTableActionType,
    ElTableColumn,
)
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
                    user_token_menu(),
                    permission_menu(),
                ],
            ),
            ElMenuItem(
                title="系统设置",
                key="dict",
                icon="ant-design:database-outlined",
                path="/dict",
                component="TableView",
                children=[
                    set_dict_menu(),
                    set_dict_group_menu(),
                ],
            ),
        ]
    )


def set_dict_group_menu():
    return ElMenuItem(
        title="字典组设置",
        key="dict-group",
        path="/set/dict-group",
        component="TableView",
        table=ElTable(
            title="字典组设置",
            columns=[
                ElTableColumn(prop="name", label="名称", width="180"),
                ElTableColumn(
                    prop="key",
                    label="key",
                    width="180",
                ),
                ElTableColumn(
                    prop="description",
                    label="描述",
                    width="180",
                ),
            ],
            search=ElForm(
                title="search",
                rows=[
                    [
                        ElFormItem(
                            label="名称",
                            prop="name",
                            placeholder="请输入名称",
                        ),
                        ElFormItem(
                            label="描述",
                            prop="description",
                            placeholder="请输入描述",
                        ),
                        # id
                        ElFormItem(
                            label="id",
                            prop="id",
                            type="input",
                            placeholder="请输入",
                            hidden=True,
                        ),
                    ]
                ],
            ),
            actions=[
                DefActions.EDIT,
                ElTableAction(
                    label="查看字典",
                    form_key="",
                    api_key="",
                    icon="ant-design:search",
                    path="/set/dict",
                    type=ElTableActionType.ROUTER,
                    props={
                        "target": "_blank",
                        "query_key": "group_id",
                        "query_value": "id",
                    },
                ),
                DefActions.DELETE,
            ],
        ),
        api=ElApis(
            list="/dict-group.list",
            delete="/dict-group.delete",
            create="/dict-group.create",
            update="/dict-group.update",
            export="/dict-group.export",
        ),
        forms={
            "create": ElForm(
                title="创建字典组",
                rows=[
                    [
                        ElFormItem(
                            label="名称",
                            prop="name",
                            type="input",
                            placeholder="请输入",
                        ),
                        ElFormItem(
                            label="key",
                            prop="key",
                            type="input",
                            placeholder="请输入",
                        ),
                        ElFormItem(
                            label="描述",
                            prop="description",
                            type="input",
                            placeholder="请输入",
                        ),
                    ],
                ],
            ),
        },
    )


def set_dict_menu():
    return ElMenuItem(
        title="字典设置",
        key="dict",
        path="/set/dict",
        component="TableView",
        table=ElTable(
            title="字典设置",
            columns=[
                ElTableColumn(prop="name", label="名称", width="180"),
                ElTableColumn(
                    prop="description",
                    label="描述",
                    width="180",
                ),
                ElTableColumn(
                    prop="key",
                    label="key",
                    width="180",
                ),
                ElTableColumn(
                    prop="value",
                    label="value",
                    width="180",
                ),
                ElTableColumn(
                    prop="group_name",
                    label="分组",
                    width="180",
                    type="link",
                    props={
                        "url_prefix": "/#/set/dict-group?id=",
                        "url_id": "group_id",
                    },
                ),
            ],
            search=ElForm(
                title="search",
                rows=[
                    [
                        # group_id
                        ElFormItem(
                            label="分组",
                            prop="group_id",
                            type="select",
                            width="240px",
                            props={
                                "remoteDataApi": "/dict-group.list",
                            },
                        ),
                        ElFormItem(
                            label="名称",
                            prop="name",
                            placeholder="请输入名称",
                        ),
                    ]
                ],
            ),
            filters=ElForm(
                title="filters",
                rows=[],
            ),
        ),
        api=ElApis(
            list="/dict.list",
            delete="/dict.delete",
            create="/dict.create",
            update="/dict.update",
            export="/dict.export",
        ),
        forms={
            "create": ElForm(
                title="创建字典",
                rows=[
                    [
                        ElFormItem(
                            label="名称",
                            prop="name",
                            type="input",
                            placeholder="请输入",
                            tips="请输入字典名称",
                        ),
                        ElFormItem(
                            label="描述",
                            prop="description",
                            type="input",
                            placeholder="请输入",
                            tips="请输入字典描述",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="key",
                            prop="key",
                            type="input",
                            placeholder="请输入",
                            tips="key 用于唯一标识字典,推荐使用 group_name 作为前缀 <br> 例如: group_name.key <a href='/' target='_blank'>查看更多</a>",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="value",
                            prop="value",
                            type="textarea",
                            placeholder="请输入",
                            width="80%"
                        ),
                    ],
                    [
                        ElFormItem(
                            label="Group",
                            prop="group_id",
                            type="select",
                            width="320px",
                            props={
                                "remoteDataApi": "/dict-group.list",
                            },
                        ),
                    ],
                ],
            ),
        },
    )


def permission_menu():
    return ElMenuItem(
        title="用户权限",
        key="permission",
        path="/permission",
        component="TableView",
        table=ElTable(
            title="权限",
            columns=[
                ElTableColumn(prop="name", label="名称", width="180"),
                ElTableColumn(
                    prop="codename", label="codename", width="180", type="tag"
                ),
                ElTableColumn(
                    prop="content_type_code",
                    label="内容类型",
                    type="tag",
                    props={"type": "info"},
                ),
            ],
        ),
        api=ElApis(
            list="/permission.list",
            delete="/permission.delete",
            create="/permission.create",
            update="/permission.update",
            export="/permission.export",
        ),
        forms={
            "create": ElForm(
                title="创建权限",
                rows=[
                    [
                        ElFormItem(
                            label="名称",
                            prop="name",
                            type="input",
                            placeholder="请输入",
                            required=True,
                            message="请输入权限名称",
                        ),
                        ElFormItem(
                            label="codename",
                            prop="codename",
                            type="input",
                            placeholder="请输入",
                            required=True,
                            message="请输入权限 Code",
                        ),
                        # content_type_id
                        ElFormItem(
                            label="content_type_id",
                            prop="content_type_id",
                            type="input",
                            placeholder="请输入",
                            hidden=True,
                            defaultValue=settings.PERMISSION_DEFAULT_CONTENT_TYPE_ID,
                        ),
                    ]
                ],
            ),
        },
    )


def user_token_menu():
    return ElMenuItem(
        title="用户登录日志",
        key="user-log",
        path="/user/user-log",
        component="TableView",
        api=ElApis(
            list="/user-log.list", export="/user-log.export", delete="/user-log.delete"
        ),
        table=ElTable(
            title="用户登录日志",
            columns=[
                # username
                ElTableColumn(prop="username", label="用户名", width="180"),
                # device
                ElTableColumn(prop="device", label="设备", type="tag"),
                # browser
                ElTableColumn(
                    prop="browser",
                    label="浏览器",
                    type="tag",
                    sortable=True,
                    width="180px",
                ),
                # version
                ElTableColumn(prop="version", label="版本", width="150px"),
                # language
                ElTableColumn(
                    prop="language", label="语言", sortable=True, width="240px"
                ),
                # user_agent
                ElTableColumn(prop="ua_cut", label="UserAgent", width="180"),
                # ip
                ElTableColumn(prop="ip", label="IP", type="link"),
                # expire_at
                ElTableColumn(
                    prop="expire_at", label="过期时间", width="180", sortable=True
                ),
            ],
            actions=[DefActions.DELETE],
            search=ElForm(
                title="search",
                rows=[
                    [
                        ElFormItem(
                            label="用户名",
                            prop="user__username",
                            placeholder="请输入用户名",
                        ),
                        ElFormItem(
                            label="IP",
                            prop="ip",
                            placeholder="请输入IP",
                        ),
                    ]
                ],
            ),
            filters=ElForm(
                title="filters",
                rows=[
                    [
                        ElFormItem(
                            label="设备",
                            prop="device",
                            type="radio-button",
                            placeholder="请选择",
                            width="180px",
                            options=[
                                {"label": "All", "value": ""},
                                {"label": "Mac", "value": "mac"},
                                {"label": "Windows", "value": "windows"},
                                {"label": "Linux", "value": "linux"},
                                {"label": "Android", "value": "android"},
                                {"label": "iOS", "value": "ios"},
                            ],
                        ),
                        ElFormItem(
                            label="浏览器",
                            prop="browser__in",
                            type="checkbox",
                            placeholder="请选择",
                            width="180px",
                            options=[
                                {"label": "Chrome", "value": "chrome"},
                                {"label": "Safari", "value": "safari"},
                                {"label": "Firefox", "value": "firefox"},
                                {"label": "IE", "value": "ie"},
                            ],
                        ),
                    ]
                ],
            ),
        ),
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
            search=ElForm(
                title="search",
                rows=[
                    [
                        ElFormItem(
                            label="用户名",
                            prop="username",
                            placeholder="请输入用户名",
                        ),
                        ElFormItem(
                            label="邮箱",
                            prop="email",
                            placeholder="请输入邮箱",
                        ),
                    ]
                ],
            ),
        ),
        api=ElApis(
            list="/user.list",
            delete="/user.delete",
            export="/user.export",
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
            export="/user-group.export",
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
