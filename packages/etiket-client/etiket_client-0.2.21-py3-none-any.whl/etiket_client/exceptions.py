class LoginFailedException(Exception):
    pass

class TokenRefreshException(Exception):
    pass

class NoAccessTokenFoundException(Exception):
    pass

class RequestFailedException(Exception):
    def __init__(self, status_code, message, *args: object) -> None:
        super().__init__(*args)
        self.status_code = status_code
        self.message = message

class uploadFailedException(Exception):
    pass

class SchemaNotValidException(Exception):
    pass