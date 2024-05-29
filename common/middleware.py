from django.http import HttpRequest

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