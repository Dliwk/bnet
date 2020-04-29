class BNetException(Exception):
    pass


class LocalApiError(BNetException):
    pass


class LocalApi:
    class DuplicateError(LocalApiError):
        def __init__(self, *args, duptype):
            super().__init__(*args)
            self.duptype = duptype
    
    class ForbiddenError(LocalApiError):
        pass

    class PasswordError(LocalApiError):
        pass

    class InvalidCall(LocalApiError):
        pass

    class NoUserError(LocalApiError):
        pass

    class InvalidPasswordError(LocalApiError):
        pass

    class NotFoundError(LocalApiError):
        pass
