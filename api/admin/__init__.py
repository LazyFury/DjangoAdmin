from common.api import Api
from common.middleware import auth_middleware, get_user_middleware, request_aspects
from common.router import Router
from core.models import User

api = Router(prefix="/admin/api")
api.use(request_aspects, sort=0)
api.use(get_user_middleware, sort=3)
api.use(auth_middleware, sort=2)

Api(User).register(api, "/user")


from .menu import *  # noqa: F401, E402, F403
from .user import *  # noqa: F401, E402, F403

