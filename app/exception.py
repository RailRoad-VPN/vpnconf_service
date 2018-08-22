import sys

sys.path.insert(0, '../rest_api_library')
from response import APIErrorEnum

name = 'VPNC-'
i = 0


def count():
    global i
    i += 1
    return i


class VPNCError(APIErrorEnum):
    __version__ = 1

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    UNKNOWN_ERROR_CODE = (name + str(count()), 'UNKNOWN_ERROR_CODE phrase', 'UNKNOWN_ERROR_CODE description')

    REQUEST_NO_JSON = (name + str(count()),  'REQUEST_NO_JSON phrase', 'REQUEST_NO_JSON description')

    VPNSERVER_FIND_ERROR_DB = (name + str(count()),  'FIND_ERROR_DB phrase', 'FIND_ERROR_DB description')
    VPNSERVER_FIND_BY_UUID_ERROR_DB = (name + str(count()),  'FIND_BY_UUID_ERROR_DB phrase', 'FIND_BY_UUID_ERROR_DB description')
    VPNSERVER_FIND_BY_UUID_ERROR = (name + str(count()),  'FIND_BY_UUID_ERROR phrase', 'FIND_BY_UUID_ERROR description')
    VPNSERVER_FIND_BY_STATUS_ID_DB = (name + str(count()),  'FIND_BY_STATUS_ID_DB phrase', 'FIND_BY_STATUS_ID_DB description')
    VPNSERVER_FIND_BY_TYPE_ID_DB = (name + str(count()),  'FIND_BY_TYPE_ID_DB phrase', 'FIND_BY_TYPE_ID_DB description')
    VPNSERVER_CREATE_ERROR_DB = (name + str(count()),  'CREATE_ERROR_DB phrase', 'CREATE_ERROR_DB description')
    VPNSERVER_UPDATE_ERROR_DB = (name + str(count()),  'UPDATE_ERROR_DB phrase', 'UPDATE_ERROR_DB description')
    VPNSERVER_IDENTIFIER_ERROR = (name + str(count()),  'VPNSERVER_IDENTIFIER_ERROR phrase', 'VPNSERVER_IDENTIFIER_ERROR description')

    VPNSERVERSMETA_FIND_ERROR_DB = (name + str(count()),  'VPNSERVERSMETA_FIND_ERROR_DB phrase', 'VPNSERVERSMETA_FIND_ERROR_DB description')

    VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB = (name + str(count()),  'VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB phrase', 'VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB description')
    VPNSERVERCONFIG_FIND_BY_UUID_ERROR = (name + str(count()),  'VPNSERVERCONFIG_FIND_BY_UUID_ERROR phrase', 'VPNSERVERCONFIG_FIND_BY_UUID_ERROR description')
    VPNSERVERCONFIG_FIND_ERROR_DB = (name + str(count()),  'VPNSERVERCONFIG_FIND_ERROR_DB phrase', 'VPNSERVERCONFIG_FIND_ERROR_DB description')
    VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR = (name + str(count()),  'VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR phrase', 'VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR description')
    VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR_DB = (name + str(count()),  'VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR_DB phrase', 'VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR_DB description')
    VPNSERVERCONFIG_CREATE_ERROR_DB = (name + str(count()),  'VPNSERVERCONFIG_CREATE_ERROR_DB phrase', 'VPNSERVERCONFIG_CREATE_ERROR_DB description')
    VPNSERVERCONFIG_UPDATE_ERROR_DB = (name + str(count()),  'VPNSERVERCONFIG_UPDATE_ERROR_DB phrase', 'VPNSERVERCONFIG_UPDATE_ERROR_DB description')
    VPNSERVERCONFIG_IDENTIFIER_ERROR = (name + str(count()),  'VPNSERVERCONFIG_IDENTIFIER_ERROR phrase', 'VPNSERVERCONFIG_IDENTIFIER_ERROR description')
    VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR_DB = (name + str(count()),  'VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR_DB phrase', 'VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR_DB description')
    VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR = (name + str(count()),  'VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR phrase', 'VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR description')
    VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR_DB = (name + str(count()),  'VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR_DB phrase', 'VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR_DB description')
    VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR = (name + str(count()),  'VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR phrase', 'VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR description')

    VPNSERVERCONN_FIND_BY_UUID_ERROR_DB = (name + str(count()),  'VPNSERVERCONN_FIND_BY_UUID_ERROR_DB phrase', 'VPNSERVERCONN_FIND_BY_UUID_ERROR_DB description')
    VPNSERVERCONN_FIND_BY_UUID_ERROR = (name + str(count()),  'VPNSERVERCONN_FIND_BY_UUID_ERROR phrase', 'VPNSERVERCONN_FIND_BY_UUID_ERROR description')
    VPNSERVERCONN_FIND_ERROR_DB = (name + str(count()),  'VPNSERVERCONN_FIND_ERROR_DB phrase', 'VPNSERVERCONN_FIND_ERROR_DB description')
    VPNSERVERCONN_FIND_BY_SERVER_UUID_ERROR = (name + str(count()),  'VPNSERVERCONN_FIND_BY_SERVER_UUID_ERROR phrase', 'VPNSERVERCONN_FIND_BY_SERVER_UUID_ERROR description')
    VPNSERVERCONN_FIND_BY_SERVER_UUID_ERROR_DB = (name + str(count()),  'VPNSERVERCONN_FIND_BY_SERVER_UUID_ERROR_DB phrase', 'VPNSERVERCONN_FIND_BY_SERVER_UUID_ERROR_DB description')
    VPNSERVERCONN_CREATE_ERROR_DB = (name + str(count()),  'VPNSERVERCONN_CREATE_ERROR_DB phrase', 'VPNSERVERCONN_CREATE_ERROR_DB description')
    VPNSERVERCONN_UPDATE_ERROR_DB = (name + str(count()),  'VPNSERVERCONN_UPDATE_ERROR_DB phrase', 'VPNSERVERCONN_UPDATE_ERROR_DB description')
    VPNSERVERCONN_IDENTIFIER_ERROR = (name + str(count()),  'VPNSERVERCONN_IDENTIFIER_ERROR phrase', 'VPNSERVERCONN_IDENTIFIER_ERROR description')
    VPNSERVERCONN_FIND_USER_CONN_ERROR_DB = (name + str(count()),  'VPNSERVERCONN_FIND_USER_CONN_ERROR_DB phrase', 'VPNSERVERCONN_FIND_USER_CONN_ERROR_DB description')
    VPNSERVERCONN_FIND_USER_CONN_ERROR = (name + str(count()),  'VPNSERVERCONN_FIND_USER_CONN_ERROR phrase', 'VPNSERVERCONN_FIND_USER_CONN_ERROR description')
    VPNSERVERCONN_FIND_BY_SERVER_AND_USER_DEVICE_ERROR_DB = (name + str(count()),  'VPNSERVERCONN_FIND_BY_SERVER_AND_USER_DEVICE_ERROR_DB phrase', 'VPNSERVERCONN_FIND_BY_SERVER_AND_USER_DEVICE_ERROR_DB description')
    VPNSERVERCONN_FIND_BY_SERVER_AND_USER_DEVICE_ERROR = (name + str(count()),  'VPNSERVERCONN_FIND_BY_SERVER_AND_USER_DEVICE_ERROR phrase', 'VPNSERVERCONN_FIND_BY_SERVER_AND_USER_DEVICE_ERROR description')
    VPNSERVERCONN_FIND_BY_SERVER_AND_VIRTUAL_IP_ERROR_DB = (name + str(count()),  'VPNSERVERCONN_FIND_BY_SERVER_AND_VIRTUAL_IP_ERROR_DB phrase', 'VPNSERVERCONN_FIND_BY_SERVER_AND_VIRTUAL_IP_ERROR_DB description')
    VPNSERVERCONN_FIND_BY_SERVER_AND_VIRTUAL_IP_ERROR = (name + str(count()),  'VPNSERVERCONN_FIND_BY_SERVER_AND_VIRTUAL_IP_ERROR phrase', 'VPNSERVERCONN_FIND_BY_SERVER_AND_VIRTUAL_IP_ERROR description')
    VPNSERVERCONN_FIND_BY_USER_DEVICE_DB = (name + str(count()),  'VPNSERVERCONN_FIND_BY_USER_DEVICE_DB phrase', 'VPNSERVERCONN_FIND_BY_USER_DEVICE_DB description')

    VPNSERVERSTATUS_FIND_ERROR_DB = (name + str(count()),  'VPNSERVERSTATUS_FIND_ERROR_DB phrase', 'VPNSERVERSTATUS_FIND_ERROR_DB description')
    VPNSERVERSTATUS_FIND_BY_ID_ERROR_DB = (name + str(count()),  'VPNSERVERSTATUS_FIND_BY_ID_ERROR_DB phrase', 'VPNSERVERSTATUS_FIND_BY_ID_ERROR_DB description')
    VPNSERVERSTATUS_FIND_BY_ID_ERROR = (name + str(count()),  'VPNSERVERSTATUS_FIND_BY_ID_ERROR phrase', 'VPNSERVERSTATUS_FIND_BY_ID_ERROR description')
    VPNSERVERSTATUS_IDENTIFIER_ERROR = (name + str(count()),  'VPNSERVERSTATUS_FIND_BY_ID_ERROR phrase', 'VPNSERVERSTATUS_FIND_BY_ID_ERROR description')
    VPNSERVERSTATUS_FIND_BY_CODE_ERROR = (name + str(count()),  'VPNSERVERSTATUS_FIND_BY_CODE_ERROR phrase', 'VPNSERVERSTATUS_FIND_BY_CODE_ERROR description')
    VPNSERVERSTATUS_FIND_BY_CODE_ERROR_DB = (name + str(count()),  'VPNSERVERSTATUS_FIND_BY_CODE_ERROR_DB phrase', 'VPNSERVERSTATUS_FIND_BY_CODE_ERROR_DB description')

    VPNTYPE_FIND_ERROR_DB = (name + str(count()),  'VPNTYPE_FIND_ERROR_DB phrase', 'VPNTYPE_FIND_ERROR_DB description')
    VPNTYPE_FIND_BY_ID_ERROR_DB = (name + str(count()),  'VPNTYPE_FIND_BY_ID_ERROR_DB phrase', 'VPNTYPE_FIND_BY_ID_ERROR_DB description')
    VPNTYPE_FIND_BY_ID_ERROR = (name + str(count()),  'VPNTYPE_FIND_BY_ID_ERROR phrase', 'VPNTYPE_FIND_BY_ID_ERROR description')
    VPNTYPE_IDENTIFIER_ERROR = (name + str(count()),  'VPNTYPE_IDENTIFIER_ERROR phrase', 'VPNTYPE_IDENTIFIER_ERROR description')

    VPN_DEVICE_PLATFORM_FIND_ERROR_DB = (name + str(count()),  'VPN_DEVICE_PLATFORM_FIND_ERROR_DB phrase', 'VPN_DEVICE_PLATFORM_FIND_ERROR_DB description')
    VPN_DEVICE_PLATFORM_FIND_BY_ID_ERROR_DB = (name + str(count()),  'VPN_DEVICE_PLATFORM_FIND_BY_ID_ERROR_DB phrase', 'VPN_DEVICE_PLATFORM_FIND_BY_ID_ERROR_DB description')
    VPN_DEVICE_PLATFORM_FIND_BY_ID_ERROR = (name + str(count()),  'VPN_DEVICE_PLATFORM_FIND_BY_ID_ERROR phrase', 'VPN_DEVICE_PLATFORM_FIND_BY_ID_ERROR description')
    VPN_DEVICE_PLATFORM_IDENTIFIER_ERROR = (name + str(count()),  'VPN_DEVICE_PLATFORM_IDENTIFIER_ERROR phrase', 'VPN_DEVICE_PLATFORM_IDENTIFIER_ERROR description')

    CITY_FIND_ERROR_DB = (name + str(count()),  'CITY_FIND_ERROR_DB phrase', 'CITY_FIND_ERROR_DB description')
    CITY_FIND_BY_UUID_ERROR_DB = (name + str(count()),  'CITY_FIND_BY_UUID_ERROR_DB phrase', 'CITY_FIND_BY_UUID_ERROR_DB description')
    CITY_FIND_BY_UUID_ERROR = (name + str(count()),  'CITY_FIND_BY_UUID_ERROR phrase', 'CITY_FIND_BY_UUID_ERROR description')
    CITY_CREATE_ERROR_DB = (name + str(count()),  'CITY_CREATE_ERROR_DB phrase', 'CITY_CREATE_ERROR_DB description')
    CITY_UPDATE_ERROR_DB = (name + str(count()),  'CITY_UPDATE_ERROR_DB phrase', 'CITY_UPDATE_ERROR_DB description')
    CITY_CREATE_ERROR = (name + str(count()),  'CITY_CREATE_ERROR phrase', 'CITY_CREATE_ERROR description')
    CITY_FINDBYID_ERROR = (name + str(count()),  'CITY_FINDBYID_ERROR phrase', 'CITY_FINDBYID_ERROR description')
    CITY_IDENTIFIER_ERROR = (name + str(count()),  'CITY_IDENTIFIER_ERROR phrase', 'CITY_IDENTIFIER_ERROR description')

    COUNTRY_FIND_ERROR_DB = (name + str(count()),  'COUNTRY_FIND_ERROR_DB phrase', 'COUNTRY_FIND_ERROR_DB description')
    COUNTRY_FIND_BY_UUID_ERROR_DB = (name + str(count()),  'COUNTRY_FIND_BY_UUID_ERROR_DB phrase', 'COUNTRY_FIND_BY_UUID_ERROR_DB description')
    COUNTRY_FIND_BY_UUID_ERROR = (name + str(count()),  'COUNTRY_FIND_BY_UUID_ERROR phrase', 'COUNTRY_FIND_BY_UUID_ERROR description')
    COUNTRY_CREATE_ERROR_DB = (name + str(count()),  'COUNTRY_CREATE_ERROR_DB phrase', 'COUNTRY_CREATE_ERROR_DB description')
    COUNTRY_UPDATE_ERROR_DB = (name + str(count()),  'COUNTRY_UPDATE_ERROR_DB phrase', 'COUNTRY_UPDATE_ERROR_DB description')
    COUNTRY_IDENTIFIER_ERROR = (name + str(count()),  'COUNTRY_IDENTIFIER_ERROR phrase', 'COUNTRY_IDENTIFIER_ERROR description')
    COUNTRY_FIND_BY_CODE_ERROR_DB = (name + str(count()),  'COUNTRY_FIND_BY_CODE_ERROR_DB phrase', 'COUNTRY_FIND_BY_CODE_ERROR_DB description')
    COUNTRY_FIND_BY_CODE_ERROR = (name + str(count()),  'COUNTRY_FIND_BY_CODE_ERROR phrase', 'COUNTRY_FIND_BY_CODE_ERROR description')
    COUNTRY_FIND_BY_STRCODE_ERROR_DB = (name + str(count()),  'COUNTRY_FIND_BY_STRCODE_ERROR_DB phrase', 'COUNTRY_FIND_BY_STRCODE_ERROR_DB description')
    COUNTRY_FIND_BY_STRCODE_ERROR = (name + str(count()),  'COUNTRY_FIND_BY_STRCODE_ERROR phrase', 'COUNTRY_FIND_BY_STRCODE_ERROR description')

    STATE_FIND_ERROR_DB = (name + str(count()),  'STATE_FIND_ERROR_DB phrase', 'STATE_FIND_ERROR_DB description')
    STATE_FIND_BY_UUID_ERROR_DB = (name + str(count()),  'STATE_FIND_BY_UUID_ERROR_DB phrase', 'STATE_FIND_BY_UUID_ERROR_DB description')
    STATE_FIND_BY_UUID_ERROR = (name + str(count()),  'STATE_FIND_BY_UUID_ERROR phrase', 'STATE_FIND_BY_UUID_ERROR description')
    STATE_CREATE_ERROR_DB = (name + str(count()),  'STATE_CREATE_ERROR_DB phrase', 'STATE_CREATE_ERROR_DB description')
    STATE_UPDATE_ERROR_DB = (name + str(count()),  'STATE_UPDATE_ERROR_DB phrase', 'STATE_UPDATE_ERROR_DB description')
    STATE_IDENTIFIER_ERROR = (name + str(count()),  'STATE_UPDATE_ERROR_DB phrase', 'STATE_UPDATE_ERROR_DB description')

    GEO_FIND_ERROR_DB = (name + str(count()),  'GEO_FIND_ERROR_DB phrase', 'GEO_FIND_ERROR_DB description')
    GEO_FIND_BY_ID_ERROR_DB = (name + str(count()),  'GEO_FIND_BY_ID_ERROR_DB phrase', 'GEO_FIND_BY_ID_ERROR_DB description')
    GEO_FIND_BY_ID_ERROR = (name + str(count()),  'GEO_FIND_BY_ID_ERROR phrase', 'GEO_FIND_BY_ID_ERROR description')
    GEO_CREATE_ERROR_DB = (name + str(count()),  'GEO_CREATE_ERROR_DB phrase', 'GEO_CREATE_ERROR_DB description')
    GEO_UPDATE_ERROR_DB = (name + str(count()),  'GEO_UPDATE_ERROR_DB phrase', 'GEO_UPDATE_ERROR_DB description')
    GEO_IDENTIFIER_ERROR = (name + str(count()),  'GEO_IDENTIFIER_ERROR phrase', 'GEO_IDENTIFIER_ERROR description')


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