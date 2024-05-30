from common.utils.contextholder import ContextHolder
from . import api

@api.get("/profile")
def profile(request):
    return {
        "user":ContextHolder.get_context_kv_pre_request(request,"user"),
    }