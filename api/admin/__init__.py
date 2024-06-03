from common.api import Api
from common.middleware import auth_middleware, get_user_middleware, request_aspects
from common.router import Router
from common.utils import dict_utils
from core.models import User, UserToken
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext as t
import json

from modules.settings.models import Dict, DictGroup

api = Router(prefix="/admin/api")
api.use(request_aspects, sort=0)
api.use(get_user_middleware, sort=3)
api.use(auth_middleware, sort=2)


def get_permission_content_type_str(permission: Permission):
    return f"{t(permission.content_type.app_label)}.{t(permission.content_type.model)}"


Api(
    User,
    config=Api.Config(
        enable_delete=False,
    ),
    hidden=["password"]
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

Api(DictGroup).register(api, "/dict-group")
Api(Dict,get_update_params=lambda request:dict_utils.filter_with_not_allow_keys({
    **json.loads(request.body)
},["group"])).register(api, "/dict")

from .menu import *  # noqa: F401, E402, F403
from .user import *  # noqa: F401, E402, F403
