import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class VPNType(object):
    __version__ = 1

    _sid = None
    _code = None
    _description = None

    def __init__(self, sid: int = None, code: str = None, description: str = None):
        self._sid = sid
        self._code = code
        self._description = description

    def to_api_dict(self):
        return {
            'id': self._sid,
            'code': self._code,
            'description': self._description,
        }

    def to_dict(self):
        return {
            'id': self._sid,
            'code': self._code,
            'description': self._description,
        }


class VPNTypeStored(StoredObject, VPNType):
    __version__ = 1

    def __init__(self, storage_service: StorageService, sid: int = None, code: str = None, description: str = None,
                 limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        VPNType.__init__(self, sid=sid, code=code, description=description)


class VPNTypeDB(VPNTypeStored):
    __version__ = 1

    _sid_field = 'id'
    _code_field = 'code'
    _description_field = 'description'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        self.logger.info('VPNTypeDB find method')
        select_sql = 'SELECT * FROM public.vpn_type'
        if self._limit:
            select_sql += "\nLIMIT %s\nOFFSET %s" % (self._limit, self._offset)
        self.logger.debug(f"{self.__class__}: Select SQL: {select_sql}")

        try:
            self.logger.debug('Call database service')
            vpntype_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = VPNCError.VPNTYPE_FIND_ERROR_DB.message
            error_code = VPNCError.VPNTYPE_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNTYPE_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        vpnserverconfig_list = []

        for vpnserverconfig_db in vpntype_list_db:
            vpnserverconfig = self.__map_vpntypedb_to_vpntype(vpnserverconfig_db)
            vpnserverconfig_list.append(vpnserverconfig)

        if len(vpnserverconfig_list) == 0:
            logging.warning('Empty VPNType list of method find. Very strange behaviour.')

        return vpnserverconfig_list

    def find_by_sid(self):
        self.logger.info('VPNTypeDB find_by_sid method')
        select_sql = 'SELECT * FROM public.vpn_type WHERE id = ?'
        self.logger.debug(f"{self.__class__}: Select SQL: {select_sql}")
        params = (self._sid,)

        try:
            self.logger.debug('Call database service')
            vpntype_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNTYPE_FIND_BY_ID_ERROR_DB.message
            error_code = VPNCError.VPNTYPE_FIND_BY_ID_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERSTATUS_FIND_BY_ID_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(vpntype_list_db) == 1:
            vpntype_db = vpntype_list_db[0]
        elif len(vpntype_list_db) == 0:
            error_message = VPNCError.VPNTYPE_FIND_BY_ID_ERROR.message
            error_code = VPNCError.VPNTYPE_FIND_BY_ID_ERROR.code
            developer_message = VPNCError.VPNTYPE_FIND_BY_ID_ERROR.developer_message
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = VPNCError.VPNTYPE_FIND_BY_ID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % VPNCError.VPNTYPE_FIND_BY_ID_ERROR.developer_message
            error_code = VPNCError.VPNTYPE_FIND_BY_ID_ERROR.code
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_vpntypedb_to_vpntype(vpntype_db)

    def __map_vpntypedb_to_vpntype(self, vpnserverstatusdb):
        return VPNType(
            sid=vpnserverstatusdb[self._sid_field],
            code=vpnserverstatusdb[self._code_field],
            description=vpnserverstatusdb[self._description_field],
        )
