# ref: https://github.com/LiViz-cc/lvz-backend/blob/main/errors.py

class ServerError(Exception):
    def __init__(self, title, status, detail):
        self.title = title
        self.status = status
        self.detail = detail


class InvalidParamError(ServerError):
    def __init__(self, detail):
        super().__init__('Invalid Parameter', 400, detail)


class NotMutableError(InvalidParamError):
    def __init__(self, class_name: str, object_name: str):
        super().__init__('Field {} in Class {} is not mutable.'.format(object_name, class_name))


class EmailAlreadyExistsError(ServerError):
    def __init__(self, email):
        super().__init__('Email Already Exists', 400,
                         'User with email address {} already exists.'.format(email))


class NotFoundError(ServerError):
    def __init__(self, target, queries):
        super().__init__('Not Found', 404,
                         '{} with {} not found.'.format(str(target).capitalize(), queries))


class UnauthorizedError(ServerError):
    def __init__(self):
        super().__init__('Unauthorized', 401, 'Cannot authorize with given credentials.')


class ForbiddenError(ServerError):
    def __init__(self, detail=""):
        if detail == "":
            detail = 'Cannot access with given authorization.'
        super().__init__('Forbidden', 403, detail)


class NotFinishedYet(Exception):
    """
    A remark for codes working in progress
    """
    pass
