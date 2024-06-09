from drakaina.exceptions import InternalServerError
from drakaina.exceptions import InvalidTokenError


class JWTBackendError(InternalServerError):
    """JWT backend error"""


class InvalidJWTTokenError(InvalidTokenError):
    """Invalid JWT token error"""


class ValidationJWTTokenError(InvalidJWTTokenError):
    """JWT token validation error"""
