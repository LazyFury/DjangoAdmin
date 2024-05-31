import inspect
from typing import Any, Callable
import uuid
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.db.models.query import QuerySet
from common.wrapped import Wrapped
from django.utils import timezone
from datetime import datetime


class Serozalizer:
    extra: dict[str, Callable[[Any], Any]]
    hidden: list[str]

   

    def __init__(self, obj, extra: dict[str, Callable[[Any], Any]] = {}, hidden=[]):
        """尝试自动遍历 obj 并转换为 json

        Args:
            obj (_type_): _description_
            extra (dict[str, Callable[[Any], Any]], optional): _description_. Defaults to None.
        """
        self.obj = obj
        self.extra = extra or {}
        self.hidden = hidden

    def convert(self, obj):
        if obj is None:
            return None
        # print(obj,type(obj))
        if isinstance(obj, (int, float, str)):
            return obj
        if isinstance(obj, ImageFieldFile):
            return obj.url if obj else None
        if isinstance(obj, datetime):
            return timezone.localtime(obj).strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, dict):
            return {k: self.convert(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [self.convert(item) for item in obj]
        if isinstance(obj,uuid.UUID):
            return str(obj)
        if isinstance(obj, object):
            return serizalize(obj)
        raise Exception(f"无法解析的类型:{type(obj)}")

    def serialize(self):
        data = {
            k: v
            for k, v in self._serizlize()
            if k not in self.hidden
        }
        return data

    def _serizlize(self):
        for field in self.fields():
            yield (
                field,
                self.convert(getattr(self.obj, field))
                if hasattr(self.obj, field)
                else None,
            )

        for field, func in self.extra.items():
            yield field, self.convert(func(self.obj))

        for method in self.methods():
            yield method.func.__name__, self.convert(method(self.obj))

    def fields(self):
        for field in vars(self.obj) if hasattr(self.obj,"__dict__") else dir(self.obj):
            if not field.startswith("_"):
                yield field

    def methods(self):
        for method,_ in inspect.getmembers(self.obj):
            if not method.startswith("_"):
                if hasattr(self.obj, method) and isinstance(
                    getattr(self.obj, method), Wrapped
                ):
                    wrapped: Wrapped = getattr(self.obj, method)
                    if wrapped.ext.get("json", True):
                        yield wrapped


class ModelSerozalizer(Serozalizer):
    obj: models.Model
    with_foreign_keys: bool
    with_relations: bool

    def __init__(
        self,
        obj,
        extra: dict[str, Callable[[Any], Any]] = {},
        with_foreign_keys: bool = True,
        with_relations: bool = False,
        **kwargs,
    ):
        """尝试自动遍历 Model 并转换为 json

        Args:
            obj (_type_): _description_
            extra (dict[str, Callable[[Any], Any]], optional): _description_. Defaults to None.
            with_foreign_keys (bool, optional): _description_. Defaults to True.
            with_relations (bool, optional): _description_. Defaults to True.
        """
        super().__init__(obj, extra, **kwargs)
        self.with_foreign_keys = with_foreign_keys
        self.with_relations = with_relations

    def fields(self):
        for field in self.obj._meta.get_fields():
            if hasattr(self.obj, field.name) and not field.is_relation:
                yield field.name

    def relations(self):
        for field in self.obj._meta.get_fields():
            if hasattr(self.obj, field.name) and field.is_relation:
                yield field

    def serialize(self):
        return super().serialize()

    def _serizlize(self):
        yield from super()._serizlize()
        
        for relation in self.relations():
            # print(relation.name,getattr(self.obj, relation.name))

            if (relation.one_to_one or relation.many_to_one) and self.with_foreign_keys:
                yield relation.name, serizalize(getattr(self.obj, relation.name),with_foreign_keys=False,with_relations=False) if getattr(self.obj, relation.name) else None
            if (
                relation.one_to_many or relation.many_to_many
            ) and self.with_relations:
                yield relation.name, serizalize(getattr(self.obj, relation.name).all(),with_foreign_keys=False,with_relations=False) if getattr(self.obj, relation.name) else None

        for k, v in self.extra.items():
            yield k, v(self.obj)


def serizalize(
    obj,
    extra: dict[str, Callable[[Any], Any]] = {},
    with_foreign_keys: bool = True,
    with_relations: bool = False,
    hidden=[],
):
    """自动解析对象为 json

    Args:
        obj (_type_): _description_
        extra (dict[str, Callable[[Any], Any]], optional): _description_. Defaults to None.
        with_foreign_keys (bool, optional): _description_. Defaults to True.
        with_relations (bool, optional): _description_. Defaults to False.
        hidden (list, optional): _description_. Defaults to [].

    Returns:
        _type_: _description_
    """
    # print("尝试解析:",type(obj))
    if isinstance(obj, (str, int, float,type(None))):
        return obj
    
    if isinstance(obj, (list, tuple, QuerySet,set)):
        return [serizalize(item,with_foreign_keys=False,with_relations=False) for item in obj]
    
    if isinstance(obj, models.Model):
        return ModelSerozalizer(
            obj,
            extra=extra,
            with_foreign_keys=with_foreign_keys,
            with_relations=with_relations,
            hidden=hidden,
        ).serialize()
    if isinstance(obj, (object, dict)):
        return Serozalizer(obj, extra=extra, hidden=hidden).serialize()
    return str(obj)
