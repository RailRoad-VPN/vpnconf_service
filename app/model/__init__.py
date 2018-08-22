from enum import Enum


class VPNServerStatusEnum(Enum):
    __version__ = 1

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, sid, name, description):
        self.sid = sid
        self.name = name
        self.description = description

    UNKNOWN = (0, 'unknown', 'Unknown, for reports only')
    OP = (1, 'op', 'Operational')
    REMOVED = (2, 'removed', 'Removed of service')
    MAINTENANCE = (3, 'maintenance', 'Under Maintenance')
    OP_NNC = (4, 'op_nnc', 'Operational. No new connections available, preparing for Maintenance')
    OP_TEST = (5, 'op_test', 'Operational; test mode')
    REMOVED_TEST = (6, 'removed_test', 'Removed of service; test mode')
    MAINTENANCE_TEST = (7, 'maintenance_test', 'Under Maintenance; test mode')
    OP_NNC_TEST = (8, 'op_nnc_test', 'Operational. No new connections available, preparing for Maintenance; test mode')


class VPNTypeEnum(Enum):
    __version__ = 1

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, sid, type_name, description):
        self.sid = sid
        self.type_name = type_name
        self.description = description

    UNKNOWN = (0, 'unknown', 'Unknown, for reports only')
    OPENVPN = (1, 'openvpn', 'Standard OpenVPN server')
    IPSECIKEV2 = (2, 'ikev2', 'IPSec w IKEv2')
