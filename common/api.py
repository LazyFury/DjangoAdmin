from typing import Any, Callable
from django.db import models
from django.http import HttpRequest
from django.db.models.query import QuerySet
from django.contrib.auth.models import AbstractUser

from common import serizalize
from common.exception import ApiNotFoundError
from common.response import ApiJsonResponse
from common.router import Router


class Api:
    class Config:
        enable_create = True
        enable_update = True
        enable_delete = True

        def __init__(self, enable_create=True, enable_update=True, enable_delete=True):
            self.enable_create = enable_create
            self.enable_update = enable_update
            self.enable_delete = enable_delete

    model: models.Model
    get_list_params: Callable[[HttpRequest], dict]
    get_create_params: Callable[[HttpRequest], dict]
    get_update_params: Callable[[HttpRequest], dict]
    extra: dict[str, Callable[[models.Model], Any]]
    hidden: list[str]
    config: Config

    def __init__(
        self,
        model: models.base.ModelBase,
        get_list_params: Callable[[HttpRequest], dict] = lambda request: {
            **request.GET.dict(),
        },
        get_create_params: Callable[[HttpRequest], dict] = lambda request: {
            **request.POST.dict()
        },
        get_update_params: Callable[[HttpRequest], dict] = lambda request: {
            **request.POST.dict()
        },
        extra: dict[str, Callable[[models.Model], Any]] = {},
        config: Config = Config(),
        hidden: list[str] = [],
    ):
        """ __init__ method for Api

        Args:
            model (models.base.ModelBase): _description_ 数据模型
            get_list_params (_type_, optional): _description_. Defaults to lambdarequest:{ **request.GET.dict(), }.
            get_create_params (_type_, optional): _description_. Defaults to lambdarequest:{ **request.POST.dict() }.
            get_update_params (_type_, optional): _description_. Defaults to lambdarequest:{ **request.POST.dict() }.
            extra (dict[str, Callable[[models.Model], Any]], optional): _description_. Defaults to {}.
            config (Config, optional): _description_. Defaults to Config().
            hidden (list[str], optional): _description_. Defaults to [].
        """
        self.model = model # type: ignore pylance 检测类型，数据模型总是 ModelBase，实际上是 Model，而且 ModelBase 也没有 orm 方法
        self.get_list_params = get_list_params
        self.get_create_params = get_create_params
        self.get_update_params = get_update_params
        self.extra = extra
        self.config = config
        self.hidden = hidden

    def extra_search_condition(self, request: HttpRequest):
        """多余的查询条件，比如从 header 获取 user_id，添加到查询条件中

        Args:
            request (HttpRequest): _description_

        Returns:
            _type_: _description_
        """
        return {}
    
    def serizalize(self, obj):
        return serizalize.serizalize(obj, extra=self.extra, hidden=self.hidden)

    def get(self, request: HttpRequest):
        id = request.GET.get("id")
        if not id:
            raise ApiNotFoundError("id is required")
        obj = self.model.objects.filter(**self.extra_search_condition(request)).get(
            pk=id
        )
        if obj:
            return ApiJsonResponse.success(
                self.serizalize(obj)
            )
        raise ApiNotFoundError()

    def list_order_by(self, query: QuerySet, orders: list[str]):
        for order in orders:
            key, order = order.split("__")
            if order == "desc":
                query = query.order_by(f"-{key}")
            else:
                query = query.order_by(key)
        return query

    def modify_query(self, query: QuerySet):
        return query

    def list(self, request: HttpRequest):
        params = self.get_list_params(request)
        page = int(params.pop("page", 1))
        size = int(params.pop("size", 10))
        orders = str(params.pop("order_by", "id__desc")).split(",")

        query = self.model.objects.filter(**params).filter(
            **self.extra_search_condition(request)
        )
        query = self.list_order_by(query, orders)
        query = self.modify_query(query)

        # print sql 
        print(query.query)

        total = query.count()
        data = query[(page - 1) * size : page * size]
        page_count = total // size + 1 if total % size > 0 else total // size
        return ApiJsonResponse.success(
            {
                "data": [
                    self.serizalize(obj) for obj in data
                ],
                "pageable": {
                    "total": total,
                    "page": page,
                    "size": size,
                    "page_count": page_count,
                },
            }
        )

    def create(self, request: HttpRequest):
        if not self.config.enable_create:
            raise ApiNotFoundError("Create is not allowed")
        params = self.get_create_params(request)
        obj = self.model.objects.create(**params)
        return ApiJsonResponse.success(self.serizalize(obj))

    def update(self, request: HttpRequest):
        if not self.config.enable_update:
            raise ApiNotFoundError("Update is not allowed")
        id = request.GET.get("id")
        if not id:
            raise ApiNotFoundError("id is required")
        obj = self.model.objects.filter(**self.extra_search_condition(request)).get(
            pk=id
        )
        if not obj:
            raise ApiNotFoundError()
        params = self.get_update_params(request)
        for key, value in params.items():
            setattr(obj, key, value)
        obj.save()
        return ApiJsonResponse.success(self.serizalize(obj))

    def delete(self, request: HttpRequest):
        if not self.config.enable_delete:
            raise ApiNotFoundError("Delete is not allowed")
        ids = request.POST.getlist("ids", [])
        if not ids:
            raise ApiNotFoundError("ids is required")
        query = self.model.objects.filter(
            **self.extra_search_condition(request)
        ).filter(pk__in=ids)
        query.delete()
        return ApiJsonResponse.success("Delete Success")

    def register(self, router: Router, path=None):
        if not path:
            path = f"/{self.model._meta.model_name}"
        print("register path:", path)
        router.get(f"{path}.detail")(self.get)
        router.get(f"{path}.list")(self.list)
        router.post(f"{path}.create")(self.create)
        router.put(f"{path}.update")(self.update)
        router.delete(f"{path}.delete")(self.delete)
        return self


class ReadOnlyApi(Api):
    def __init__(self, model: models.base.ModelBase, **kwargs):
        super().__init__(model, config=Api.Config(enable_create=False, enable_update=False, enable_delete=False), **kwargs)

class PreUserApi(Api):
    forgen_user_field:str

    def __init__(self, model: models.base.ModelBase, forgen_user_field="user_id", **kwargs):
        super().__init__(model, **kwargs)
        self.forgen_user_field = forgen_user_field

    def extra_search_condition(self, request: HttpRequest):
        user = request.user
        if not user.is_authenticated:
            raise ApiNotFoundError("Not Authenticated")
        assert isinstance(user,AbstractUser)
        return {self.forgen_user_field:user.pk}
    
    def register(self, router: Router, path=None):
        if not path:
            path = f"/{self.model._meta.model_name}"
        print("register path:", path)
        router.get(f"{path}.detail")(per_user_api_wrapper(self.get))
        router.get(f"{path}.list")(per_user_api_wrapper(self.list))
        router.post(f"{path}.create")(per_user_api_wrapper(self.create))
        router.put(f"{path}.update")(per_user_api_wrapper(self.update))
        router.delete(f"{path}.delete")(per_user_api_wrapper(self.delete))
        return self
    
def per_user_api_wrapper(func):
    def wrapper(request: HttpRequest):
        if not request.user.is_authenticated:
            return ApiJsonResponse.error("Not Authenticated",401)
        return func(request)
    return wrapper