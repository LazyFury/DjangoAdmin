from django.http import JsonResponse
from common.router import Router
from common.utils.contextholder import ContextHolder
import django

api = Router("/api/v1")


def cors_middleware(request, get_response):
    def wrapper(request):
        # text context holder 
        ContextHolder.set_context_kv("user", request.user or {
            "username": "anonymous",
            "is_authenticated": False,
        })
        ContextHolder.set_context_kv("path",request.path)
        response = get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = (
            "Content-Type, X-CSRFToken, Authorization,TOKEN"
        )
        response["Access-Control-Max-Age"] = "86400"
        return response

    return wrapper


api.use(cors_middleware) # add cors middleware


@api.get("/hello")
def hello(request):
    user = ContextHolder.get_context_kv("user")
    return JsonResponse(
        {
            "message": "Hello, World!",
            "user": {
                "name":user.username
            },
            "path":ContextHolder.get_context_kv("path"),
            "thread_name":ContextHolder.get_context_kv("thread_name"),
            "version":django.get_version()
        }
    )


@api.get("/info")
def hello_name(request):
    return JsonResponse(
        {
            "name": "Django",
            "version": "3.2.7",
        }
    )
