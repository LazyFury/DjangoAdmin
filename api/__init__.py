import datetime
from django.http import JsonResponse
from common.middleware import cors_middleware
from common.router import Router
from common.serizalize import ModelSerozalizer, serizalize
from common.utils.contextholder import ContextHolder
import django

api = Router("/api/v1")


api.use(cors_middleware)  # add cors middleware

def clear_context_each_request(get_response):
    """ clear_context_each_request

    Args:
        get_response (_type_): _description_
    """
    def wrapper(request):
        print("clear context.")
        response = get_response(request)
        ContextHolder.set_context_pre_request(request,{})
        return response

    return wrapper

def get_user_middleware(get_response):
    """ get_user_middleware

    Args:
        get_response (_type_): _description_
    """
    def wrapper(request):
        user = request.user
        print("get User:",user)
        ContextHolder.set_context_kv_pre_request(request, "user", user)
        response = get_response(request)
        return response

    return wrapper

def request_aspects(get_response):
    """ request_aspects

    Args:
        get_response (_type_): _description_
    """
    def wrapper(request):
        print("request Start:",datetime.datetime.now())
        response = get_response(request)
        print("request End.",datetime.datetime.now())
        return response

    return wrapper

api.use(clear_context_each_request,sort=0)
api.use(request_aspects,sort=0)
api.use(get_user_middleware,sort=1)

@api.get("/hello")
def hello(request):
    user = ContextHolder.get_context_kv_pre_request(request,"user")
    ContextHolder.set_context_kv_pre_request(request, "count", 1)
    # print(ContextHolder.get_context())

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
                    "groups": lambda obj: [group.name for group in obj.groups.all()]
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
