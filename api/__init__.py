from django.db.models.base import Model as Model
from django.http import JsonResponse
from common.api import Api
from common.middleware import clear_context_each_request, cors_middleware, get_user_middleware, request_aspects
from common.router import Router
from common.serizalize import ModelSerozalizer, serizalize
from common.utils.contextholder import ContextHolder
import django
from django.contrib.auth.models import Group, Permission
from core.models import User

api = Router("/api/v1")


api.use(cors_middleware)  # add cors middleware
api.use(clear_context_each_request,sort=0) # 清理每次请求的上下文
api.use(request_aspects,sort=0) # 请求切面
api.use(get_user_middleware,sort=1) # 获取用户信息

Api(User,hidden=['password'],extra={
    "groups": lambda obj: [serizalize(group,with_relations=True,with_foreign_keys=True) for group in obj.groups.all()], # type: ignore
}).register(api)


# 直接注册 Group 和 Permission
Api(Group).register(api)
Api(Permission).register(api)

@api.register("/groups")
class GroupApi(Api):
    """ 注解注册 crud 接口

    Args:
        Api (_type_): _description_
    """
    def __init__(self, *args, **kwargs):
        super().__init__(Group, *args, **kwargs)

@api.get("/hello")
def hello(request):
    user:User = ContextHolder.get_context_kv_pre_request(request,"user") # type: ignore
    return JsonResponse(
        {
            "message": "Hello, World!",
            "user": getattr(user, "username", "default"),
            "path": ContextHolder.get_context_kv("path"),
            "thread_name": ContextHolder.get_context_kv("thread_name"),
            "version": django.get_version(),
            "users": ModelSerozalizer(
                user,
                extra={
                    "groups": lambda obj: [serizalize(group,with_relations=True,with_foreign_keys=True) for group in obj.groups.all()],
                    "all_permissions": lambda user:[
                        serizalize(permission,with_relations=True,with_foreign_keys=True,extra={
                            "code":lambda obj:f"{obj.content_type.app_label}.{obj.codename}",
                        }) for permission in user.get_all_permissions()
                    ] if user else None,
                },
                hidden=["password"],
            ).serialize() if user else None,
            "count": ContextHolder.get_context_kv_pre_request(request, "count"),
        }
    )


@api.get("/info")
def hello_name(request):
    return JsonResponse(
        {
            "name": "Django",
            "version": django.get_version(),
            "thread_name": ContextHolder.get_context_kv("thread_name"),
            "count": ContextHolder.get_context_kv_pre_request(request, "count"),
        }
    )
