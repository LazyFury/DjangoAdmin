from django.http import HttpRequest

from api.admin.ui.article import (
    cms_article_category_menu,
    cms_article_edit_menu,
    cms_article_menu,
    cms_article_tag_menu,
)
from api.admin.ui.product import (
    product_attr_group_menu,
    product_attr_menu,
    product_attr_value_menu,
    product_brand_menu,
    product_category_menu,
    product_list_menu,
    product_service_menu,
    product_sku_menu,
    product_sku_value_menu,
    product_tag_menu,
)
from api.admin.ui.user import user_group_menu, user_menu, user_token_menu
from app import settings
from libs.elementui.base import ElApis
from libs.elementui.form import ElForm, ElFormItem
from libs.elementui.menu import ElMenu, ElMenuGap, ElMenuItem
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
                title="内容管理",
                key="cms",
                icon="ant-design:file-text-outlined",
                path="/cms",
                component="SubMenuView",
                children=[
                    cms_article_menu(),
                    cms_article_category_menu(),
                    cms_article_tag_menu(),
                    cms_article_edit_menu(),
                ],
            ),
            ElMenuItem(
                title="商品管理",
                key="products",
                icon="ant-design:shopping-outlined",
                path="/products",
                component="SubMenuView",
                children=[
                    product_list_menu(),
                    product_category_menu(),
                    ElMenuItem(
                        title="商品规格",
                        key="product-sku",
                        path="/products/product-sku",
                        component="TableView",
                        children=[
                            product_sku_menu(),
                            product_sku_value_menu(),
                        ]
                    ),
                    ElMenuGap("其他设置"),
                    ElMenuItem(
                        title="商品属性",
                        key="product-attr-menu",
                        path="/products/product-attr-menu",
                        component="-",
                        children=[
                            product_attr_group_menu(),
                            product_attr_menu(),
                            product_attr_value_menu(),
                        ],
                    ),
                    product_brand_menu(),
                    product_tag_menu(),
                    product_service_menu(),
                ],
            ),
            ElMenuItem(
                title="用户管理",
                key="user",
                icon="ant-design:user-outline",
                path="/user",
                component="SubMenuView",
                children=[
                    user_menu(),
                    user_group_menu(),
                    user_token_menu(),
                    permission_menu(),
                ],
            ),
            ElMenuItem(
                title="系统设置",
                key="set",
                icon="ant-design:setting-outlined",
                path="/set",
                component="SubMenuView",
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
                    param_keys=[{"group_id": "id"}],
                    type=ElTableActionType.ROUTER,
                    props={
                        "target": "_blank",
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
                            width="80%",
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
        path="/user/permission",
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

