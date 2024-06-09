from enum import Enum

from .base_models import BaseSQLModel


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    TEST = "TEST"


class User(BaseSQLModel, table=True):
    name: str
    role: UserRole
