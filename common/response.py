import json
from django.http import HttpResponse, JsonResponse

from common import serizalize
from common.exception import ApiBadRequestError, ApiError


class ApiJsonResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        if data is not None: 
            if isinstance(data, object):
                data = serizalize.serizalize(data)

        super().__init__(json.dumps(data,sort_keys=False),**kwargs)
        self["content-type"] = "application/json"

    def status(self, code):
        self.status_code = code
        return self

    class Data:
        def __init__(self, data, message, success, code):
            self.data = data
            self.message = message
            self.success = success
            self.code = code

    @staticmethod
    def success(data, message="", code=200, http_code=200):
        return ApiJsonResponse(ApiJsonResponse.Data(data, message, True, code)).status(
            http_code
        )

    @staticmethod
    def error(message, code=400, http_code=200, data=None):
        return ApiJsonResponse(ApiJsonResponse.Data(data, message, False, code)).status(
            http_code
        )
    
    @staticmethod
    def is_valid_http_code(http_code):
        return http_code >= 100 and http_code < 600

    @staticmethod
    def error_response(error: ApiError):
        if not isinstance(error, ApiError):
            error = ApiBadRequestError(str(error))
        return ApiJsonResponse(
            ApiJsonResponse.Data(None, error.message, False, error.code)
        ).status(error.code if ApiJsonResponse.is_valid_http_code(error.code) else 400)
