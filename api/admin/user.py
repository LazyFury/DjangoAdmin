import json
from common.exception import ApiForbiddenError, ApiNotAuthorizedError
from common.response import ApiJsonResponse
from common.utils.contextholder import ContextHolder
from common.validate import StrValidateRule, Validator
from core.models import UserToken
from core.services.auth import AuthService
from . import api


@api.get("/profile")
def profile(request):
    if not request.user.is_authenticated:
        return ApiNotAuthorizedError("Not Authenticated")
    return {
        "user": ContextHolder.get_context_kv_pre_request(request, "user"),
    }


@api.post("/login")
def login(request):
    params = Validator(
        rules=[
            StrValidateRule("username", "Username is required", required=True,validator=lambda x: x.strip()),
            StrValidateRule("password", "Password is required", required=True),
        ]
    ).validate(json.loads(request.body))
    password = params.pop("password", "")
    assert password, "Password is required"
    user = AuthService().authenticate(email=params["username"], password=password)
    request.user = user
    if not user.is_superuser:
        raise ApiForbiddenError("无权限")
    return {
        "user": user,
        "token": UserToken.get_fresh_token_by_user(user, request=request).token,
    }


@api.post("/logout")
def logout(request):
    token = request.headers.get("TOKEN")
    UserToken.set_invalid_by_token(token)
    return ApiJsonResponse.success("Logout Success")