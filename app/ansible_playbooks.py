from enum import Enum


class AnsiblePlaybook(Enum):
    __version__ = 1

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, sid, name):
        self.sid = sid
        self.name = name

    CREATE_AND_REGISTER_USER_CERT = (1, '', '')
    WITHDRAW_USER_CERT = (2, '', '')