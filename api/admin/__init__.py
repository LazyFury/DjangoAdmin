from common.api import Api
from common.middleware import auth_middleware, get_user_middleware, is_superuser_middleware, request_aspects
from common.router import Router
from common.utils import dict_utils
from core.models import User, UserToken
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext as t
import json

from modules.posts.models import Article, ArticleCategory, ArticleTag
from modules.settings.models import Dict, DictGroup

api = Router(prefix="/admin/api")
api.use(request_aspects, sort=0)
api.use(get_user_middleware, sort=3)
api.use(auth_middleware, sort=2)
api.use(is_superuser_middleware,sort=4)


def get_permission_content_type_str(permission: Permission):
    return f"{t(permission.content_type.app_label)}.{t(permission.content_type.model)}"


# 用户管理
Api(
    User,
    config=Api.Config(
        enable_delete=False,
    ),
    hidden=["password"],
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
    get_update_params=lambda request: dict_utils.filter_with_not_allow_keys(
        dict_utils.modify_with_callback(
            {
                **json.loads(request.body),
            },
            {
                "tag_ids": lambda data: ",".join(data.get("tag_ids", [])),
            },
        ),
        ["author", "category"],
    ),
    get_create_params=lambda request: dict_utils.modify_with_callback(
        {
            **json.loads(request.body),
        },
        {
            "tag_ids": lambda data: ",".join(data.get("tag_ids", [])),
        },
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

from .menu import *  # noqa: F401, E402, F403
from .user import *  # noqa: F401, E402, F403
