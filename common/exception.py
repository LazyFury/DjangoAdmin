class ApiError(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


class ApiNotFoundError(ApiError):
    def __init__(self, message="Not Found", code=404):
        super().__init__(message, code)


class ApiBadRequestError(ApiError):
    def __init__(self, message="Bad Request", code=400):
        super().__init__(message, code)


class ApiNotAuthorizedError(ApiError):
    def __init__(self, message="Not Authorized", code=401):
        super().__init__(message, code)


class ApiForbiddenError(ApiError):
    def __init__(self, message="Forbidden", code=403):
        super().__init__(message, code)
