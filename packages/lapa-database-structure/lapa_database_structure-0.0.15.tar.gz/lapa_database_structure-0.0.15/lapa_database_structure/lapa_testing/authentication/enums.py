from enum import Enum


class UserAccountStatusEnum(Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"


class UserLogEventEnum(Enum):
    CREATED = "CREATED"
    DELETED = "DELETED"
