
from libs.elementui.base import ElApis, ElPage
from libs.elementui.form import ElForm, ElFormItem
from libs.elementui.menu import ElMenuItem
from libs.elementui.table import DefActions, ElTable, ElTableAction, ElTableActionType, ElTableColumn

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
                    props={"url_prefix": "mailto:"},
                ),
                ElTableColumn(prop="is_active", label="is_active", type="checkbox"),
            ],
            search=ElForm(
                title="search",
                rows=[
                    [
                        ElFormItem(
                            label="用户名",
                            prop="username__contains",
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
            update="/user.update",
        ),
        forms={
            "update": ElForm(
                title="创建用户",
                rows=[
                    [
                        # avatar
                        ElFormItem(
                            label="头像",
                            prop="avatar",
                            type="upload-image",
                            placeholder="请选择头像",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="用户名",
                            prop="username",
                            type="input",
                            placeholder="请输入用户名",
                            required=True,
                            message="请输入用户名",
                        ),
                    ],
                ],
            ),
        },
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
