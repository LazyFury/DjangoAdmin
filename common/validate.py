from typing import Callable


class ValidateRule:
    prop: str
    type: str
    message: str
    required: bool
    validator: Callable | None

    def __init__(
        self,
        prop: str,
        type: str,
        message: str,
        required: bool = True,
        validator: Callable | None = None,
    ) -> None:
        self.prop = prop
        self.type = type
        self.message = message
        self.required = required
        self.validator = validator

    def validate(self, value):
        if self.required and value is None:
            return False
        if self.validator and callable(self.validator):
            return self.validator(value)
        return True


class StrValidateRule(ValidateRule):
    def __init__(self, prop: str, message: str, required: bool = True,**kwargs) -> None:
        super().__init__(prop, "string", message, required,**kwargs)

    def validate(self, value):
        if not super().validate(value):
            return False
        if not isinstance(value, str):
            return False
        return True


class BoolValidateRule(ValidateRule):
    def __init__(self, prop: str, message: str, required: bool = True,**kwargs) -> None:
        super().__init__(prop, "bool", message, required,**kwargs)

    def validate(self, value):
        if not super().validate(value):
            return False
        if not isinstance(value, bool):
            return False
        return True


class Validator:
    def __init__(self, rules: list[ValidateRule]) -> None:
        self.rules = rules

    def validate(self, data: dict):
        valid = {}
        for rule in self.rules:
            valid[rule.prop] = data.get(rule.prop)
            if not rule.validate(valid.get(rule.prop)):
                raise Exception(rule.message)
        return valid
