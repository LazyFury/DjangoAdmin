import datetime
from django.http import HttpRequest

from common.utils.contextholder import ContextHolder

def cors_middleware(get_response):
    def wrapper(request:HttpRequest):
        response = get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = (
            "Content-Type, X-CSRFToken, Authorization,TOKEN"
        )
        response["Access-Control-Max-Age"] = "86400"
        return response

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
        print(">>========request End.",datetime.datetime.now())
        return response

    return wrapper