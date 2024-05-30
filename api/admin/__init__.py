from common.router import Router

api = Router(prefix="/admin/api")

from .menu import menus  # noqa: F401, E402