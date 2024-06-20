
from libs.elementui.base import ElApis, ElPage
from libs.elementui.form import ElForm, ElFormItem
from libs.elementui.menu import ElMenuItem
from libs.elementui.table import DefActions, ElTable, ElTableAction, ElTableActionType, ElTableColumn


def cms_article_tag_menu():
    return ElMenuItem(
        title="文章标签",
        key="article-tag",
        path="/cms/article-tag",
        component="TableView",
        table=ElTable(
            title="文章标签",
            columns=[
                ElTableColumn(prop="tag", label="标签", width="180"),
            ],
            search=ElForm(
                title="search",
                rows=[
                    [
                        ElFormItem(
                            label="标签",
                            prop="tag",
                            placeholder="请输入标签",
                        ),
                    ]
                ],
            ),
        ),
        api=ElApis(
            list="/article-tag.list",
            delete="/article-tag.delete",
            create="/article-tag.create",
            update="/article-tag.update",
            export="/article-tag.export",
        ),
        forms={
            "create": ElForm(
                title="创建标签",
                rows=[
                    [
                        ElFormItem(
                            label="标签",
                            prop="tag",
                            type="input",
                            placeholder="请输入",
                        ),
                    ],
                ],
            ),
        },
    )


def cms_article_category_menu():
    return ElMenuItem(
        title="文章分类",
        key="article-category",
        path="/cms/article-category",
        component="TableView",
        table=ElTable(
            title="文章分类",
            columns=[
                ElTableColumn(prop="name", label="名称", width="180"),
                ElTableColumn(
                    prop="description",
                    label="描述",
                    width="180",
                ),
                ElTableColumn(
                    prop="parent_name",
                    label="父分类",
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
                DefActions.DELETE,
            ],
            expand=True,
        ),
        api=ElApis(
            list="/article-category.list",
            delete="/article-category.delete",
            create="/article-category.create",
            update="/article-category.update",
            export="/article-category.export",
        ),
        forms={
            "create": ElForm(
                title="创建分类",
                rows=[
                    [
                        ElFormItem(
                            label="名称",
                            prop="name",
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
                    [
                        ElFormItem(
                            label="父分类",
                            prop="parent_id",
                            type="cascader",
                            placeholder="请输入",
                            required=False,
                            props={
                                "remoteDataApi": "/article-category.list",
                                "multiple": False,
                                "checkStrictly": True,
                                "show-all-levels": True,
                                "clearable": True,
                            },
                        ),
                    ],
                ],
            ),
        },
    )


def cms_article_edit_menu():
    return ElMenuItem(
        title="添加/编辑文章",
        key="article-edit",
        path="/cms/article/edit",
        component="FormView",
        hidden=True,
        type=ElPage.FORM,
        currentForm="create",
        forms={
            "create": article_create_form(),
        },
    )


def cms_article_menu():
    return ElMenuItem(
        title="文章管理",
        key="article",
        path="/cms/article",
        component="TableView",
        table=ElTable(
            title="文章管理",
            columns=[
                ElTableColumn(prop="title", label="标题", width="180"),
                ElTableColumn(
                    prop="description",
                    label="描述",
                    width="180",
                ),
                ElTableColumn(
                    prop="category_name",
                    label="分类",
                    width="180",
                ),
                ElTableColumn(prop="tag_names", label="标签", width="180", type="tags"),
                # author_avatar
                ElTableColumn(
                    prop="author_avatar",
                    label="作者头像",
                    width="100",
                    type="image",
                ),
                ElTableColumn(
                    prop="author_name",
                    label="作者",
                    width="180",
                ),
                ElTableColumn(
                    prop="created_at",
                    label="创建时间",
                    width="180",
                ),
                ElTableColumn(
                    prop="updated_at",
                    label="更新时间",
                    width="180",
                ),
            ],
            search=ElForm(
                title="search",
                rows=[
                    [
                        ElFormItem(
                            label="标题",
                            prop="title",
                            placeholder="请输入标题",
                        ),
                        ElFormItem(
                            label="作者",
                            prop="author",
                            placeholder="请输入作者",
                        ),
                    ]
                ],
            ),
            filters=ElForm(
                title="filters",
                rows=[],
            ),
            actions=[
                ElTableAction(
                    label="编辑",
                    icon="ant-design:edit-outlined",
                    api_key="update|create",
                    type=ElTableActionType.ROUTER,
                    form_key="update|create",
                    path="/cms/article/edit",
                    param_keys=[{"id": "id"}],
                ),
                DefActions.DELETE,
            ],
            add_btn=ElTableAction(
                label="创建",
                icon="ant-design:plus-outlined",
                api_key="create",
                type=ElTableActionType.ROUTER,
                form_key="create",
                path="/cms/article/edit",
                param_keys=[],
            ),
        ),
        api=ElApis(
            list="/article.list",
            delete="/article.delete",
            create="/article.create",
            update="/article.update",
            export="/article.export",
        ),
        forms={
            "create": article_create_form(),
        },
    )


def article_create_form():
    return ElForm(
        title="创建文章",
        create_api="/article.create",
        update_api="/article.update",
        detail_api="/article.detail",
        detail_param_keys=["id"],
        buttons_container_class_name="",
        rows=[
            [
                ElFormItem(
                    label="标题",
                    prop="title",
                    type="input",
                    placeholder="请输入",
                    width="540px",
                    props={
                        "maxlength": 64,
                        "show-word-limit": True,
                    },
                ),
            ],
            [
                ElFormItem(
                    label="描述",
                    prop="description",
                    type="textarea",
                    placeholder="请输入",
                    width="540px",
                    required=False,
                    props={
                        "maxlength": 255,
                        "show-word-limit": True,
                    },
                ),
            ],
            [
                ElFormItem(
                    label="分类",
                    prop="category_id",
                    type="select",
                    placeholder="请输入",
                    width="320px",
                    props={
                        "remoteDataApi": "/article-category.list",
                    },
                ),
                ElFormItem(
                    label="作者",
                    prop="author_id",
                    type="select",
                    placeholder="请输入",
                    width="320px",
                    props={
                        "remoteDataApi": "/user.list",
                    },
                ),
            ],
            [
                ElFormItem(
                    label="内容",
                    prop="content",
                    type="quill",
                    placeholder="请输入",
                    width="96%",
                    props={
                        "rows": 10,
                        "style": "width: 100%;",
                    },
                ),
            ],
            [
                ElFormItem(
                    label="标签",
                    prop="tag_ids",
                    type="select",
                    placeholder="请输入",
                    required=False,
                    width="80%",
                    props={
                        "remoteDataApi": "/article-tag.list",
                        "multiple": True,
                    },
                ),
            ],
        ],
    )

