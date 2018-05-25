import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService


class VPNServersMeta(object):
    __version__ = 1

    _sid = None
    _version = None
    _state_version = None

    def __init__(self, sid: int = None, version: int = None, state_version: int = None):
        self._sid = sid
        self._version = version
        self._state_version = state_version

    def to_dict(self):
        return {
            'version': self._version,
            'state_version': self._state_version,
        }


class VPNServersMetaStored(VPNServersMeta):
    __version__ = 1

    _storage_service = None

    def __init__(self, storage_service: StorageService, **kwargs) -> None:
        super().__init__(**kwargs)

        self._storage_service = storage_service


class VPNServersMetaDB(VPNServersMetaStored):
    __version__ = 1

    _sid_field = 'id'
    _version_field = 'version'
    _state_version_field = 'state_version'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('VPNServersMetaDB find method')
        select_sql = 'SELECT * FROM public.vpnserversmeta'
        logging.debug('Select SQL: %s' % select_sql)

        try:
            logging.debug('Call database service')
            vpnserversmeta_db = self._storage_service.get(sql=select_sql)[0]
        except DatabaseError as e:
            logging.error(e)
            error_message = VPNCError.VPNSERVERSMETA_FIND_ERROR_DB.phrase
            error_code = VPNCError.VPNSERVERSMETA_FIND_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERSMETA_FIND_ERROR_DB.description, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return VPNServersMeta(
            sid=vpnserversmeta_db[self._sid_field],
            version=vpnserversmeta_db[self._version_field],
            state_version=vpnserversmeta_db[self._state_version_field],
        )
