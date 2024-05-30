import json
from common.utils.contextholder import ContextHolder
from core.models import UserToken
from core.services.auth import AuthService
from . import api

@api.get("/profile")
def profile(request):
    return {
        "user":ContextHolder.get_context_kv_pre_request(request,"user"),
    }

@api.post("/login")
def login(request):
    params = {
        **json.loads(request.body),
    }
    password = params.pop("password","")
    print(password)
    assert password,"请输入密码"
    user = AuthService().authenticate(email=params['username'],password=password)
    request.user = user
    return {
        "user":user,
        "token":UserToken.get_fresh_token_by_user(user,request=request).token,
    }