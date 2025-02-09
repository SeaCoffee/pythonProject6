class JWTException(Exception):
    pass

class JWTInvalidException(JWTException):
    def __init__(self, message="Invalid token"):
        super().__init__(message)

class JWTBlacklistException(JWTException):
    def __init__(self, message="Token is blacklisted"):
        super().__init__(message)

class JWTExpiredException(JWTException):
    def __init__(self, message="Token has expired"):
        super().__init__(message)
