import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class VPNServersMeta(object):
    __version__ = 1

    _sid = None
    _version = None
    _condition_version = None

    def __init__(self, sid: int = None, version: int = None, condition_version: int = None):
        self._sid = sid
        self._version = version
        self._condition_version = condition_version

    def to_dict(self):
        return {
            'id': self._sid,
            'version': self._version,
            'condition_version': self._condition_version,
        }

    def to_api_dict(self):
        return {
            'version': self._version,
            'condition_version': self._condition_version,
        }


class VPNServersMetaStored(StoredObject, VPNServersMeta):
    __version__ = 1

    def __init__(self, storage_service: StorageService, sid: int = None, version: int = None,
                 condition_version: int = None, limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        VPNServersMeta.__init__(self, sid=sid, version=version, condition_version=condition_version)


class VPNServersMetaDB(VPNServersMetaStored):
    __version__ = 1

    _sid_field = 'id'
    _version_field = 'version'
    _condition_version_field = 'condition_version'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('VPNServersMetaDB find method')
        select_sql = 'SELECT * FROM public.vpnserversmeta'
        if self._limit:
            select_sql += "\nLIMIT %s\nOFFSET %s" % (self._limit, self._offset)
        logging.debug(f"Select SQL: {select_sql}")

        try:
            logging.debug('Call database service')
            vpnserversmeta_db = self._storage_service.get(sql=select_sql)[0]
        except DatabaseError as e:
            logging.error(e)
            error_message = VPNCError.VPNSERVERSMETA_FIND_ERROR_DB.message
            error_code = VPNCError.VPNSERVERSMETA_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERSMETA_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return VPNServersMeta(
            sid=vpnserversmeta_db[self._sid_field],
            version=vpnserversmeta_db[self._version_field],
            condition_version=vpnserversmeta_db[self._condition_version_field],
        )
