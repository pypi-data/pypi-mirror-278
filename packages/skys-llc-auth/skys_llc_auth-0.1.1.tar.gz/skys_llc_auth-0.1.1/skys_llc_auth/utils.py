from enum import Enum
from typing import Any


class UserRole(Enum):
    Student = "Student"
    Instructor = "Instructor"
    Administrator = "Administrator"
    Server = "Server"


class TokenType(str, Enum):
    access = "access"
    refresh = "refresh"


class Singleton:  # pragma: no cover
    def __new__(cls, *args: Any, **kwds: Any):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args: Any, **kwds: Any):
        pass
