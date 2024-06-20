
from libs.elementui.base import ElApis, ElPage
from libs.elementui.form import ElForm, ElFormItem
from libs.elementui.menu import ElMenuItem
from libs.elementui.table import DefActions, ElTable, ElTableAction, ElTableActionType, ElTableColumn

def product_sku_menu():
    return ElMenuItem(
        title="商品规格",
        key="product-sku",
        path="/products/product-sku",
        component="TableView",
        table=ElTable(
            title="商品规格",
            description="商品规格是购买的时候需要选择的",
            columns=[
                ElTableColumn(prop="name", label="规格", width="180"),
                # description
                ElTableColumn(prop="description", label="描述", width="180"),
            ],
        ),
        api=ElApis(
            list="/product-sku.list",
            delete="/product-sku.delete",
            create="/product-sku.create",
            update="/product-sku.update",
            export="/product-sku.export",
        ),
        forms={
            "create": ElForm(
                title="创建规格",
                rows=[
                    [
                        ElFormItem(
                            label="规格",
                            prop="name",
                            type="input",
                            placeholder="请输入",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="描述",
                            prop="description",
                            type="textarea",
                            placeholder="请输入",
                            required=False,
                            width="80%",
                        ),
                    ],
                ],
            ),
        },
    )


def product_sku_value_menu():
    return ElMenuItem(
        title="商品规格值",
        key="product-sku-value",
        path="/products/product-sku-value",
        component="TableView",
        table=ElTable(
            title="商品规格值",
            columns=[
                ElTableColumn(prop="name", label="规格值", width="180"),
                # description
                ElTableColumn(prop="description", label="描述", width="180"),
                # sku_name
                ElTableColumn(prop="sku_name", label="规格", width="180"),
            ],
        ),
        api=ElApis(
            list="/product-sku-value.list",
            delete="/product-sku-value.delete",
            create="/product-sku-value.create",
            update="/product-sku-value.update",
            export="/product-sku-value.export",
        ),
        forms={
            "create": ElForm(
                title="创建规格值",
                rows=[
                    [
                        ElFormItem(
                            label="规格值",
                            prop="name",
                            type="input",
                            placeholder="请输入",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="描述",
                            prop="description",
                            type="textarea",
                            placeholder="请输入",
                            required=False,
                            width="80%",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="规格",
                            prop="sku_id",
                            type="select",
                            width="320px",
                            placeholder="请输入",
                            props={"remoteDataApi": "/product-sku.list"},
                        ),
                    ],
                ],
            ),
        },
    )


def product_attr_value_menu():
    return ElMenuItem(
        title="商品属性值",
        key="product-attr-value",
        path="/products/product-attr-value",
        component="TableView",
        table=ElTable(
            title="商品属性值",
            columns=[
                ElTableColumn(prop="name", label="属性值", width="180"),
                # description
                ElTableColumn(prop="description", label="描述", width="180"),
                # attr_name
                ElTableColumn(prop="attr_name", label="属性", width="180"),
            ],
        ),
        api=ElApis(
            list="/product-attr-value.list",
            delete="/product-attr-value.delete",
            create="/product-attr-value.create",
            update="/product-attr-value.update",
            export="/product-attr-value.export",
        ),
        forms={
            "create": ElForm(
                title="创建属性值",
                rows=[
                    [
                        ElFormItem(
                            label="属性值",
                            prop="name",
                            type="input",
                            placeholder="请输入",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="描述",
                            prop="description",
                            type="textarea",
                            placeholder="请输入",
                            required=False,
                            width="80%",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="属性",
                            prop="attr_id",
                            type="select",
                            placeholder="请输入",
                            width="320px",
                            props={
                                "remoteDataApi": "/product-attr.list",
                            },
                        ),
                    ],
                ],
            ),
        },
    )


def product_attr_menu():
    return ElMenuItem(
        title="商品属性",
        key="product-attr",
        path="/products/product-attr",
        component="TableView",
        table=ElTable(
            title="商品属性",
            description="商品属性仅展示/和提供搜索时筛选",
            columns=[
                ElTableColumn(prop="name", label="属性", width="180"),
                # description
                ElTableColumn(prop="description", label="描述", width="180"),
                # group_name
                ElTableColumn(prop="group_name", label="组", width="180"),
            ],
        ),
        api=ElApis(
            list="/product-attr.list",
            delete="/product-attr.delete",
            create="/product-attr.create",
            update="/product-attr.update",
            export="/product-attr.export",
        ),
        forms={
            "create": ElForm(
                title="创建属性",
                rows=[
                    [
                        ElFormItem(
                            label="属性",
                            prop="name",
                            type="input",
                            placeholder="请输入",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="描述",
                            prop="description",
                            type="textarea",
                            placeholder="请输入",
                            required=False,
                            width="80%",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="组",
                            prop="group_id",
                            type="select",
                            placeholder="请输入",
                            width="320px",
                            props={
                                "remoteDataApi": "/product-attr-group.list",
                            },
                        ),
                    ],
                ],
            ),
        },
    )


def product_attr_group_menu():
    return ElMenuItem(
        title="商品属性组",
        key="product-attr-group",
        path="/products/product-attr-group",
        component="TableView",
        table=ElTable(
            title="商品属性组",
            columns=[
                ElTableColumn(prop="name", label="组", width="180"),
                # description
                ElTableColumn(prop="description", label="描述", width="180"),
            ],
        ),
        api=ElApis(
            list="/product-attr-group.list",
            delete="/product-attr-group.delete",
            create="/product-attr-group.create",
            update="/product-attr-group.update",
            export="/product-attr-group.export",
        ),
        forms={
            "create": ElForm(
                title="创建属性组",
                rows=[
                    [
                        ElFormItem(
                            label="组",
                            prop="name",
                            type="input",
                            placeholder="请输入",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="描述",
                            prop="description",
                            type="textarea",
                            placeholder="请输入",
                            required=False,
                            width="80%",
                        ),
                    ],
                ],
            ),
        },
    )


def product_service_menu():
    return ElMenuItem(
        title="商品服务",
        key="product-service",
        path="/products/product-service",
        component="TableView",
        table=ElTable(
            title="商品服务",
            columns=[
                ElTableColumn(prop="name", label="服务", width="180"),
                # description
                ElTableColumn(prop="description", label="描述", width="180"),
            ],
        ),
        api=ElApis(
            list="/product-service.list",
            delete="/product-service.delete",
            create="/product-service.create",
            update="/product-service.update",
            export="/product-service.export",
        ),
        forms={
            "create": ElForm(
                title="创建服务",
                rows=[
                    [
                        ElFormItem(
                            label="服务",
                            prop="name",
                            type="input",
                            placeholder="请输入",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="描述",
                            prop="description",
                            type="textarea",
                            placeholder="请输入",
                            width="80%",
                        ),
                    ],
                ],
            ),
        },
    )


def product_tag_menu():
    return ElMenuItem(
        title="商品标签",
        key="product-tag",
        path="/products/product-tag",
        icon="material-symbols:bookmarks-outline",
        component="TableView",
        table=ElTable(
            title="商品标签",
            columns=[
                ElTableColumn(prop="name", label="标签", width="180"),
                # description
                ElTableColumn(prop="description", label="描述", width="180"),
            ],
        ),
        api=ElApis(
            list="/product-tag.list",
            delete="/product-tag.delete",
            create="/product-tag.create",
            update="/product-tag.update",
            export="/product-tag.export",
        ),
        forms={
            "create": ElForm(
                title="创建标签",
                rows=[
                    [
                        ElFormItem(
                            label="标签",
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
                    ]
                ],
            ),
        },
    )


def product_brand_menu():
    return ElMenuItem(
        title="商品品牌",
        key="product-brand",
        path="/products/product-brand",
        icon="tabler:brand-booking",
        component="TableView",
        table=ElTable(
            title="商品品牌",
            columns=[
                # icon
                ElTableColumn(prop="icon", label="logo", width="180", type="image"),
                ElTableColumn(prop="name", label="品牌", width="180"),
                # description
                ElTableColumn(prop="description", label="描述", width="180"),
            ],
        ),
        api=ElApis(
            list="/product-brand.list",
            delete="/product-brand.delete",
            create="/product-brand.create",
            update="/product-brand.update",
            export="/product-brand.export",
        ),
        forms={
            "create": ElForm(
                title="创建品牌",
                rows=[
                    [
                        # icon
                        ElFormItem(
                            label="logo",
                            prop="icon",
                            type="upload-image",
                            placeholder="请输入",
                            props={"multiple": False},
                        ),
                    ],
                    [
                        ElFormItem(
                            label="品牌",
                            prop="name",
                            type="input",
                            placeholder="请输入",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="描述",
                            prop="description",
                            type="textarea",
                            placeholder="请输入",
                            width="80%",
                        ),
                    ],
                ],
            ),
        },
    )


def product_category_menu():
    return ElMenuItem(
        title="商品分类",
        key="product-category",
        path="/products/product-category",
        icon="ant-design:appstore-outlined",
        component="TableView",
        table=ElTable(
            title="商品分类",
            description="商品分类列表",
            columns=[
                # icon
                ElTableColumn(prop="icon", label="logo", width="180", type="image"),
                ElTableColumn(prop="name", label="分类", width="180"),
                # description
                ElTableColumn(prop="description", label="描述", width="180"),
            ],
            search=ElForm(
                title="search",
                rows=[
                    [
                        ElFormItem(
                            label="分类",
                            prop="name",
                            placeholder="请输入分类",
                        ),
                    ]
                ],
            ),
        ),
        api=ElApis(
            list="/product-category.list",
            delete="/product-category.delete",
            create="/product-category.create",
            update="/product-category.update",
            export="/product-category.export",
        ),
        forms={
            "create": ElForm(
                title="创建分类",
                rows=[
                    [
                        # icon
                        ElFormItem(
                            label="logo",
                            prop="icon",
                            type="upload-image",
                            placeholder="请输入",
                            props={"multiple": False},
                        ),
                    ],
                    [
                        ElFormItem(
                            label="分类",
                            prop="name",
                            type="input",
                            placeholder="请输入",
                        ),
                    ],
                    [
                        ElFormItem(
                            label="描述",
                            prop="description",
                            type="textarea",
                            placeholder="请输入",
                            width="80%",
                        ),
                    ],
                    [
                        # parent_id
                        ElFormItem(
                            label="父级",
                            prop="parent_id",
                            type="select",
                            placeholder="请输入",
                            width="320px",
                            required=False,
                            props={
                                "remoteDataApi": "/product-category.list",
                                "multiple": False,
                                "clearable": True,
                            },
                        ),
                    ],
                ],
            ),
        },
    )

