from enum import IntEnum


class VPNCError(IntEnum):
    def __new__(cls, value, phrase, description=''):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        obj.description = description
        return obj

    UNKNOWN_ERROR_CODE = (0, 'UNKNOWN_ERROR_CODE phrase', 'UNKNOWN_ERROR_CODE description')

    VPNSERVER_FIND_ERROR_DB = (1, 'FIND_ERROR_DB phrase', 'FIND_ERROR_DB description')
    VPNSERVER_FIND_BY_UUID_ERROR_DB = (2, 'FIND_BY_UUID_ERROR_DB phrase', 'FIND_BY_UUID_ERROR_DB description')
    VPNSERVER_FIND_BY_UUID_ERROR = (3, 'FIND_BY_UUID_ERROR phrase', 'FIND_BY_UUID_ERROR description')
    VPNSERVER_FIND_BY_STATUS_ID_DB = (4, 'FIND_BY_STATUS_ID_DB phrase', 'FIND_BY_STATUS_ID_DB description')
    VPNSERVER_FIND_BY_TYPE_ID_DB = (5, 'FIND_BY_TYPE_ID_DB phrase', 'FIND_BY_TYPE_ID_DB description')
    VPNSERVER_CREATE_ERROR_DB = (6, 'CREATE_ERROR_DB phrase', 'CREATE_ERROR_DB description')
    VPNSERVER_UPDATE_ERROR_DB = (7, 'UPDATE_ERROR_DB phrase', 'UPDATE_ERROR_DB description')

    VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB = (8, 'VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB phrase', 'VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB description')
    VPNSERVERCONFIG_FIND_BY_UUID_ERROR = (9, 'VPNSERVERCONFIG_FIND_BY_UUID_ERROR phrase', 'VPNSERVERCONFIG_FIND_BY_UUID_ERROR description')
    VPNSERVERCONFIG_FIND_ERROR_DB = (10, 'VPNSERVERCONFIG_FIND_ERROR_DB phrase', 'VPNSERVERCONFIG_FIND_ERROR_DB description')
    VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR = (11, 'VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR phrase', 'VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR description')
    VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR_DB = (12, 'VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR_DB phrase', 'VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR_DB description')
    VPNSERVERCONFIG_CREATE_ERROR_DB = (13, 'VPNSERVERCONFIG_CREATE_ERROR_DB phrase', 'VPNSERVERCONFIG_CREATE_ERROR_DB description')
    VPNSERVERCONFIG_UPDATE_ERROR_DB = (14, 'VPNSERVERCONFIG_UPDATE_ERROR_DB phrase', 'VPNSERVERCONFIG_UPDATE_ERROR_DB description')

    VPNSERVERSTATUS_FIND_ERROR_DB = (15, 'VPNSERVERSTATUS_FIND_ERROR_DB phrase', 'VPNSERVERSTATUS_FIND_ERROR_DB description')
    VPNSERVERSTATUS_FIND_BY_ID_ERROR_DB = (16, 'VPNSERVERSTATUS_FIND_BY_ID_ERROR_DB phrase', 'VPNSERVERSTATUS_FIND_BY_ID_ERROR_DB description')
    VPNSERVERSTATUS_FIND_BY_ID_ERROR = (17, 'VPNSERVERSTATUS_FIND_BY_ID_ERROR phrase', 'VPNSERVERSTATUS_FIND_BY_ID_ERROR description')

    VPNTYPE_FIND_ERROR_DB = (18, 'VPNTYPE_FIND_ERROR_DB phrase', 'VPNTYPE_FIND_ERROR_DB description')
    VPNTYPE_FIND_BY_ID_ERROR_DB = (19, 'VPNTYPE_FIND_BY_ID_ERROR_DB phrase', 'VPNTYPE_FIND_BY_ID_ERROR_DB description')
    VPNTYPE_FIND_BY_ID_ERROR = (20, 'VPNTYPE_FIND_BY_ID_ERROR phrase', 'VPNTYPE_FIND_BY_ID_ERROR description')

    CITY_FIND_ERROR_DB = (21, 'CITY_FIND_ERROR_DB phrase', 'CITY_FIND_ERROR_DB description')
    CITY_FIND_BY_UUID_ERROR_DB = (22, 'CITY_FIND_BY_UUID_ERROR_DB phrase', 'CITY_FIND_BY_UUID_ERROR_DB description')
    CITY_FIND_BY_UUID_ERROR = (23, 'CITY_FIND_BY_UUID_ERROR phrase', 'CITY_FIND_BY_UUID_ERROR description')
    CITY_CREATE_ERROR_DB = (24, 'CITY_CREATE_ERROR_DB phrase', 'CITY_CREATE_ERROR_DB description')
    CITY_UPDATE_ERROR_DB = (25, 'CITY_UPDATE_ERROR_DB phrase', 'CITY_UPDATE_ERROR_DB description')

    COUNTRY_FIND_ERROR_DB = (26, 'COUNTRY_FIND_ERROR_DB phrase', 'COUNTRY_FIND_ERROR_DB description')
    COUNTRY_FIND_BY_UUID_ERROR_DB = (27, 'COUNTRY_FIND_BY_UUID_ERROR_DB phrase', 'COUNTRY_FIND_BY_UUID_ERROR_DB description')
    COUNTRY_FIND_BY_UUID_ERROR = (28, 'COUNTRY_FIND_BY_UUID_ERROR phrase', 'COUNTRY_FIND_BY_UUID_ERROR description')
    COUNTRY_CREATE_ERROR_DB = (29, 'COUNTRY_CREATE_ERROR_DB phrase', 'COUNTRY_CREATE_ERROR_DB description')
    COUNTRY_UPDATE_ERROR_DB = (30, 'COUNTRY_UPDATE_ERROR_DB phrase', 'COUNTRY_UPDATE_ERROR_DB description')

    STATE_FIND_ERROR_DB = (31, 'STATE_FIND_ERROR_DB phrase', 'STATE_FIND_ERROR_DB description')
    STATE_FIND_BY_UUID_ERROR_DB = (32, 'STATE_FIND_BY_UUID_ERROR_DB phrase', 'STATE_FIND_BY_UUID_ERROR_DB description')
    STATE_FIND_BY_UUID_ERROR = (33, 'STATE_FIND_BY_UUID_ERROR phrase', 'STATE_FIND_BY_UUID_ERROR description')
    STATE_CREATE_ERROR_DB = (34, 'STATE_CREATE_ERROR_DB phrase', 'STATE_CREATE_ERROR_DB description')
    STATE_UPDATE_ERROR_DB = (35, 'STATE_UPDATE_ERROR_DB phrase', 'STATE_UPDATE_ERROR_DB description')

    GEO_FIND_ERROR_DB = (36, 'GEO_FIND_ERROR_DB phrase', 'GEO_FIND_ERROR_DB description')
    GEO_FIND_BY_ID_ERROR_DB = (37, 'GEO_FIND_BY_ID_ERROR_DB phrase', 'GEO_FIND_BY_ID_ERROR_DB description')
    GEO_FIND_BY_ID_ERROR = (38, 'GEO_FIND_BY_ID_ERROR phrase', 'GEO_FIND_BY_ID_ERROR description')
    GEO_CREATE_ERROR_DB = (39, 'GEO_CREATE_ERROR_DB phrase', 'GEO_CREATE_ERROR_DB description')
    GEO_UPDATE_ERROR_DB = (40, 'GEO_UPDATE_ERROR_DB phrase', 'GEO_UPDATE_ERROR_DB description')


class VPNException(Exception):
    __version__ = 1

    error = None
    error_code = None
    developer_message = None

    def __init__(self, error: str, error_code: int, developer_message: str = None, *args):
        super().__init__(*args)
        self.error = error
        self.error_code = error_code
        self.developer_message = developer_message


class VPNNotFoundException(VPNException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)