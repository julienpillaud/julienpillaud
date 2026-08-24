from app.core.logger import logger


class APIError(Exception):
    def __init__(self, message: str) -> None:
        logger.error(message)
        super().__init__(message)


class SecurityError(APIError):
    pass


class InvalidAccessTokenError(SecurityError):
    pass


class InvalidRefreshTokenError(SecurityError):
    pass
