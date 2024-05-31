import os
import traceback
from typing import Any, Callable
from django.http import HttpRequest, HttpResponse, JsonResponse

from app import settings
from common.exception import ApiError
from common.response import ApiJsonResponse

import better_exceptions
better_exceptions.hook()

class Route:
    def __init__(self, path, method, handler):
        """__init__ method for Route

        Args:
            path (_type_): _description_
            method (_type_): _description_
            handler (_type_): _description_
        """
        self.path = path
        self.method = method
        self.handler = handler

    def match(self, path, method):
        return self.path == path and self.method == method

    def __str__(self):
        return f"Route({self.path}, {self.method}, {self.handler})"

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.handler(*args, **kwds)


class Router:
    middlewares: list[tuple[int, Callable[[Callable], Callable]]] = []
    prefix: str = ""

    def __init__(self, prefix=""):
        """__init__ method for Router

        Args:
            prefix (str, optional): _description_. Defaults to "".
        """
        self.routes = []
        self.prefix = prefix

    def add_route(self, path, method, handler):
        self.routes.append(Route(self.prefix + path, method, handler))

    def match(self, path, method):
        for route in self.routes:
            if route.match(path, method):
                return route
        return None

    def handle(self, request: HttpRequest):
        try:

            def get_response(request=request):
                route = self.match(request.path, request.method)
                if route:
                    resp = route(request)
                    if isinstance(resp, (dict, list)):
                        return ApiJsonResponse.success(resp)
                    if isinstance(resp, (str)):
                        return HttpResponse(content=resp)
                    if isinstance(resp, (HttpResponse, JsonResponse, ApiJsonResponse)):
                        return resp
                    raise ValueError("Invalid response type")
                print("not found")
                return ApiJsonResponse.error_response(ApiError("Not Found", 404))

            for _, middleware in self.middlewares:
                get_response = middleware(get_response)

            if callable(get_response):
                response = get_response(request=request)
                return response
            
            return JsonResponse(status=400, data={"message": "Invalid middleware"})
        except Exception as e:
            better_exceptions.excepthook(e.__class__, e, e.__traceback__)
            if isinstance(e, ApiError):
                return ApiJsonResponse.error_response(e)
            return ApiJsonResponse.error_response(ApiError(str(e), 500))

    def route(self, path, method):
        def wrapper(handler):
            self.add_route(path, method, handler)
            return handler

        return wrapper

    def use(self, middleware: Callable[[Callable], Callable], sort=99):
        """添加中间件

        Args:
            middleware (Callable[[Callable],Callable]): _description_
            sort (int, optional): _description_. Defaults to 99. 小于 99 先执行，否则后执行
        """
        self.middlewares.append((sort, middleware))
        self.sort_middleware()

    def sort_middleware(self):
        """middleware 是一个闭包不停套壳的过程，所以越靠后的实际上优先级越高，在最外层也就是最先执行"""
        self.middlewares = sorted(self.middlewares, key=lambda x: x[0], reverse=True)

    def get(self, path):
        return self.route(path, "GET")

    def post(self, path):
        return self.route(path, "POST")

    def put(self, path):
        return self.route(path, "PUT")

    def delete(self, path):
        return self.route(path, "DELETE")

    def patch(self, path):
        return self.route(path, "PATCH")

    def options(self, path):
        return self.route(path, "OPTIONS")

    def register(self, path):
        def wrapper(cls):
            print("register:", cls, self)
            cls().register(router=self, path=path) if hasattr(cls, "register") else None
            return cls

        return wrapper
