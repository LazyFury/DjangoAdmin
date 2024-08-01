import datetime

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse

from app import settings
from common.exception import ApiNotAuthorizedError
from common.response import ApiJsonResponse
from common.utils.contextholder import ContextHolder
from core.models import UserToken


def modify_cors_response(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response["Access-Control-Allow-Headers"] = (
        "Content-Type, X-CSRFToken, Authorization,TOKEN"
    )
    response["Access-Control-Max-Age"] = "86400"
    return response


def cors_middleware(get_response):
    def wrapper(request:HttpRequest):
        print("cors_middleware")
        if request.method == "OPTIONS":
            response = HttpResponse()
            return modify_cors_response(response)

        response = get_response(request)
        return modify_cors_response(response)

    return wrapper



def clear_context_each_request(get_response):
    """ clear_context_each_request

    Args:
        get_response (_type_): _description_
    """
    def wrapper(request):
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
        print(">>========request Start:",datetime.datetime.now(),"Url:",request.path,"Method:",request.method) 
        response = get_response(request)
        print(">>========request End.",datetime.datetime.now(),"Url:",request.path,"Method:",request.method)
        return response

    return wrapper

def auth_middleware(get_response):
    """ auth_middleware

    Args:
        get_response (_type_): _description_
    """
    def wrapper(request):
        print("auth_middleware")

        token = request.headers.get("TOKEN")
        user = None
        if token:
            user = UserToken.find_user_by_token(token)
            token = UserToken.objects.filter(token=token).first()
            
        request.user = user if user else AnonymousUser()

        if request.path not in settings.AUTH_WHITE_LIST:
            if not token:
                raise ApiNotAuthorizedError("Token not found")
            if not request.user.is_authenticated: 
                return ApiJsonResponse.error_response(ApiNotAuthorizedError())
            if not token.valid():
                raise ApiNotAuthorizedError("Token expired")
        response = get_response(request)
        return response

    return wrapper


def is_superuser_middleware(get_response):
    def wrapper(request):
        if request.path in settings.AUTH_WHITE_LIST:
            return get_response(request)
        if not request.user.is_authenticated:
            raise ApiNotAuthorizedError("Not Authenticated")
        if not request.user.is_superuser:
            raise ApiNotAuthorizedError("Not SuperUser")
        response = get_response(request)
        return response

    return wrapper