import json

from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext as t

from common.api import Api
from common.middleware import (
    auth_middleware,
    get_user_middleware,
    is_superuser_middleware,
    request_aspects,
)
from common.router import Router
from common.tools.upload import upload_handler
from common.utils import dict_utils
from core.models import User, UserToken
from modules.posts.models import Article, ArticleCategory, ArticleTag
from modules.settings.models import Dict, DictGroup
from modules.store.models import (
    Product,
    ProductAttr,
    ProductAttrGroup,
    ProductAttrValue,
    ProductBrand,
    ProductCategory,
    ProductService,
    ProductSku,
    ProductSkuValue,
    ProductTag,
)

api = Router(prefix="/admin/api")
api.use(request_aspects, sort=0)
api.use(get_user_middleware, sort=3)
api.use(auth_middleware, sort=2)
api.use(is_superuser_middleware, sort=4)


def get_permission_content_type_str(permission: Permission):
    return f"{t(permission.content_type.app_label)}.{t(permission.content_type.model)}"


api.post("/common/upload")(upload_handler)

# 用户管理
Api(
    User,
    config=Api.Config(
        enable_delete=False,
        enable_create=False,
    ),
    hidden=["password"],
    get_update_params=lambda request: dict_utils.filter_with_allow_keys(
        {**json.loads(request.body)}, ["username", "avatar", "id"]
    ),
).register(api, "/user")
Api(Group).register(api, "/user-group")
Api(UserToken).register(api, "/user-log")
Api(
    Permission,
    extra={
        "content_type_code": get_permission_content_type_str  # type: ignore
    },
    get_update_params=lambda request: dict_utils.filter_with_allow_keys(
        {**json.loads(request.body)}, ["name", "id", "codename"]
    ),
).register(api, "/permission")


# 设置
Api(DictGroup).register(api, "/dict-group")
Api(
    Dict,
    get_update_params=lambda request: dict_utils.filter_with_not_allow_keys(
        {**json.loads(request.body)}, ["group"]
    ),
).register(api, "/dict")


# 文章内容管理
Api(
    Article,
    get_create_params=lambda request: dict_utils.filter_with_allow_keys(
        dict_utils.modify_with_callback(
            {
                **json.loads(request.body),
            },
            {
                "tag_ids": lambda data: ",".join(data.get("tag_ids", [])),
            },
        ),
        ["id","title", "content","description", "category_id", "tag_ids","author_id"],
    ),
).register(api, "/article")

Api(
    ArticleCategory,
    get_list_params=lambda request: {**request.GET.dict(), "parent_id__isnull": True},
    get_update_params=lambda request: dict_utils.filter_with_allow_keys(
        {**json.loads(request.body)}, ["parent_id", "id", "name"]
    ),
    get_export_params=lambda request: {**request.GET.dict()},
).register(api, "/article-category")

Api(ArticleTag).register(api, "/article-tag")


# 商品管理
Api(
    ProductCategory,
    get_list_params=lambda request: {**request.GET.dict(), "parent_id__isnull": True},
    get_update_params=lambda request: dict_utils.filter_with_allow_keys(
        {**json.loads(request.body)}, ["parent_id", "id", "name", "icon"]
    ),
    get_export_params=lambda request: {**request.GET.dict()},
).register(api, "/product-category")
Api(ProductBrand).register(api, "/product-brand")
Api(ProductTag).register(api, "/product-tag")
Api(ProductService).register(api, "/product-service")
Api(ProductAttrGroup).register(api, "/product-attr-group")
Api(Product,
    get_create_params=lambda request:dict_utils.filter_with_not_allow_keys(
        {**json.loads(request.body)}, ["category", "brand","price_str"]
    )).register(api, "/product")

def get_product_attr_params(request):
    return dict_utils.filter_with_allow_keys(
        {**json.loads(request.body)}, ["id", "name", "description", "group_id"]
    )


Api(
    ProductAttr,
    get_create_params=get_product_attr_params,
    get_update_params=get_product_attr_params,
).register(api, "/product-attr")


def get_product_attr_value_params(request):
    return dict_utils.filter_with_allow_keys(
        {**json.loads(request.body)}, ["attr_id", "id", "name", "description"]
    )


Api(
    ProductAttrValue,
    get_create_params=get_product_attr_value_params,
    get_update_params=get_product_attr_value_params,
).register(api, "/product-attr-value")

Api(ProductSku).register(api, "/product-sku")
Api(
    ProductSkuValue,
    get_create_params=lambda request: dict_utils.filter_with_allow_keys(
        json.loads(request.body), ["id", "name", "description", "sku_id"]
    ),
).register(api, "/product-sku-value")

from .menu import *  # noqa: F401, E402, F403
from .user import *  # noqa: F401, E402, F403
