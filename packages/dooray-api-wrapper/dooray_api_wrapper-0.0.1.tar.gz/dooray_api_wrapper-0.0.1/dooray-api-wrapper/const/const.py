from enum import Enum


class Scope(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class Type(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class State(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
