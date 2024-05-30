from common.middleware import auth_middleware, cors_middleware, get_user_middleware, request_aspects
from common.router import Router

api = Router(prefix="/admin/api")
api.use(cors_middleware,sort=1)
api.use(request_aspects,sort=0)
api.use(get_user_middleware,sort=1)
api.use(auth_middleware)

from .menu import *  # noqa: F401, E402, F403
from .user import *  # noqa: F401, E402, F403