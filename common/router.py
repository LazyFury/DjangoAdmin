from typing import Any
from django.http import HttpRequest, HttpResponse, JsonResponse



class Route:
    def __init__(self, path, method, handler):
        """ __init__ method for Route

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
    middlewares: list = []
    prefix: str = ""

    def __init__(self, prefix=""):
        """ __init__ method for Router

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
        route = self.match(request.path, request.method)
        if route:
            try:
                def get_response(request=request):
                    resp = route(request)
                    if isinstance(resp, dict):
                        return JsonResponse(resp)
                    if isinstance(resp, str):
                        return HttpResponse(content=resp)
                    if isinstance(resp, (HttpResponse, JsonResponse)):
                        return resp
                    raise ValueError("Invalid response type")

                for middleware in self.middlewares:
                    get_response = middleware(request, get_response)
                if callable(get_response):
                    response = get_response(request=request)
                    return response
                return JsonResponse(status=400, data={"message": "Invalid middleware"})
            except Exception as e:
                return JsonResponse(status=500, data={"message": str(e)})
            
        return HttpResponse(status=404, content="Not Found")

    def route(self, path, method):
        def wrapper(handler):
            self.add_route(path, method, handler)
            return handler

        return wrapper

    def use(self, middleware):
        self.middlewares.append(middleware)

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
