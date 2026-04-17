class AuthorizationError(Exception):
    pass


class InvalidAccessToken(AuthorizationError):
    pass


class InvalidRefreshToken(AuthorizationError):
    pass
