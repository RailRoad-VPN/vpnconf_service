import datetime
import logging
import sys
import uuid

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService


class VPNServer(object):
    __version__ = 1

    _suuid = None
    _version = None
    _state_version = None
    _type_id = None
    _status_id = None
    _bandwidth = None
    _load = None
    _geo_position_id = None
    _created_date = None

    def __init__(self, suuid: str = None, version: int = None, state_version: int = None, type_id: int = None,
                 status_id: int = None, bandwidth: int = None, load: int = None, geo_position_id: int = None,
                 created_date: datetime = None):
        self._suuid = suuid
        self._version = version
        self._state_version = state_version
        self._type_id = type_id
        self._status_id = status_id
        self._bandwidth = bandwidth
        self._load = load
        self._geo_position_id = geo_position_id
        self._created_date = created_date

    def to_dict(self):
        return {
            'uuid': self._suuid,
            'version': self._version,
            'state_version': self._state_version,
            'type_id': self._type_id,
            'status_id': self._status_id,
            'bandwidth': self._bandwidth,
            'load': self._load,
            'geo_position_id': self._geo_position_id,
            'created_date': self._created_date,
        }


class VPNServerStored(VPNServer):
    __version__ = 1

    _storage_service = None

    def __init__(self, storage_service: StorageService, **kwargs) -> None:
        super().__init__(**kwargs)

        self._storage_service = storage_service


class VPNServerDB(VPNServerStored):
    __version__ = 1

    _suuid_field = 'uuid'
    _version_field = 'version'
    _state_version_field = 'state_version'
    _type_id_field = 'type_id'
    _status_id_field = 'status_id'
    _bandwidth_field = 'bandwidth'
    _load_field = 'load'
    _geo_position_id_field = 'geo_position_id'
    _created_date_field = 'created_date'

    __limit = None
    __offset = None

    def __init__(self, limit: int = None, offset: int = None, **kwargs):
        self.__limit = limit
        self.__offset = offset
        super().__init__(**kwargs)

    def find(self):
        logging.info('VPNServerDB find method')
        select_sql = '''
                      SELECT 
                          uuid, 
                          version, 
                          state_version, 
                          type_id, 
                          status_id, 
                          bandwidth, 
                          load, 
                          geo_position_id, 
                          to_json(created_date) AS created_date 
                      FROM public.vpnserver
                      '''
        if self.__limit:
            select_sql += "LIMIT %s\nOFFSET %s" % (self.__limit, self.__offset)
        logging.debug('Select SQL: %s' % select_sql)

        try:
            logging.debug('Call database service')
            vpnserver_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = VPNCError.VPNSERVER_FIND_ERROR_DB.phrase
            error_code = VPNCError.VPNSERVER_FIND_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (VPNCError.VPNSERVER_FIND_ERROR_DB.description, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        vpnserver_list = []

        for vpnserver_db in vpnserver_list_db:
            vpnserver = self.__map_vpnserverdb_to_vpnserver(vpnserver_db)
            vpnserver_list.append(vpnserver)

        if len(vpnserver_list) == 0:
            logging.warning('Empty VPNServers list of method find_all. Very strange behaviour.')

        return vpnserver_list

    def find_by_suuid(self):
        logging.info('Find VPNServer by uuid')
        select_sql = '''
                      SELECT 
                          uuid, 
                          version, 
                          state_version, 
                          type_id, 
                          status_id, 
                          bandwidth, 
                          load, 
                          geo_position_id, 
                          to_json(created_date) AS created_date 
                      FROM public.vpnserver 
                      WHERE uuid = ?
                      '''
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._suuid,)

        try:
            logging.debug('Call database service')
            vpnserver_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR_DB.phrase
            error_code = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVER_FIND_BY_UUID_ERROR_DB.description, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(vpnserver_list_db) == 1:
            vpnserver_db = vpnserver_list_db[0]
        elif len(vpnserver_list_db) == 0:
            error_message = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR.phrase
            error_code = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR.value
            developer_message = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR.description
            raise VPNNotFoundException(error=error_message, error_code=error_code,
                                       developer_message=developer_message)
        else:
            error_message = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR.phrase
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % VPNCError.VPNSERVER_FIND_BY_UUID_ERROR.description
            error_code = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR.value
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_vpnserverdb_to_vpnserver(vpnserver_db)

    def find_by_status_id(self):
        logging.info('Find VPNServer by uuid')
        select_sql = '''
                      SELECT 
                          uuid, 
                          version, 
                          state_version, 
                          type_id, 
                          status_id, 
                          bandwidth, 
                          load, 
                          geo_position_id, 
                          to_json(created_date) AS created_date 
                      FROM public.vpnserver 
                      WHERE status_id = ?
                      '''
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._status_id,)

        try:
            logging.debug('Call database service')
            vpnserver_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVER_FIND_BY_STATUS_ID_DB.phrase
            error_code = VPNCError.VPNSERVER_FIND_BY_STATUS_ID_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVER_FIND_BY_STATUS_ID_DB.description, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        vpnserver_list = []

        for vpnserver_db in vpnserver_list_db:
            vpnserver = self.__map_vpnserverdb_to_vpnserver(vpnserver_db)
            vpnserver_list.append(vpnserver)

        if len(vpnserver_list) == 0:
            logging.warning('Empty VPNServers list of method find by status id. Very strange behaviour.')

        return vpnserver_list

    def find_by_type_id(self):
        logging.info('Find VPNServer by uuid')
        select_sql = '''
                      SELECT 
                          uuid, 
                          version, 
                          state_version, 
                          type_id, 
                          status_id, 
                          bandwidth, 
                          load, 
                          geo_position_id, 
                          to_json(created_date) AS created_date 
                      FROM public.vpnserver 
                      WHERE type_id = ?
                      '''
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._type_id,)

        try:
            logging.debug('Call database service')
            vpnserver_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVER_FIND_BY_TYPE_ID_DB.phrase
            error_code = VPNCError.VPNSERVER_FIND_BY_TYPE_ID_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVER_FIND_BY_TYPE_ID_DB.description, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        vpnserver_list = []

        for vpnserver_db in vpnserver_list_db:
            vpnserver = self.__map_vpnserverdb_to_vpnserver(vpnserver_db)
            vpnserver_list.append(vpnserver)

        if len(vpnserver_list) == 0:
            logging.warning('Empty VPNServers list of method find by status id. Very strange behaviour.')

        return vpnserver_list

    def create(self):
        self._suuid = uuid.uuid4()
        logging.info('Create object VPNServer with uuid: ' + str(self._suuid))
        insert_sql = '''
                      INSERT INTO public.vpnserver 
                        (uuid, type_id, status_id, bandwidth, geo_position_id, load) 
                      VALUES 
                        (?, ?, ?, ?, ?, ?)
                     '''
        insert_params = (
            self._suuid,
            self._type_id,
            self._status_id,
            self._bandwidth,
            self._geo_position_id,
            self._load,
        )
        logging.debug('Create VPNServer SQL : %s' % insert_sql)

        try:
            logging.debug('Call database service')
            self._storage_service.create(sql=insert_sql, data=insert_params)
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVER_CREATE_ERROR_DB.phrase
            error_code = VPNCError.VPNSERVER_CREATE_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (VPNCError.VPNSERVER_CREATE_ERROR_DB.description, e.pgcode, e.pgerror)

            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('VPNServer created.')

        return self._suuid

    def update(self):
        logging.info('Update VPNServer')

        update_sql = '''
                    UPDATE public.vpnserver 
                    SET type_id = ?,
                        status_id = ?,
                        bandwidth = ?,
                        geo_position_id = ?,
                        load = ?
                    WHERE 
                      uuid = ?
                    RETURNING version, state_version;
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._type_id,
            self._status_id,
            self._bandwidth,
            self._geo_position_id,
            self._load,
            self._suuid,
        )

        try:
            logging.debug("Call database service")
            updated = self._storage_service.update(sql=update_sql, data=update_params, is_return=True)
            updated = updated[0]
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVER_UPDATE_ERROR_DB.phrase
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (VPNCError.VPNSERVER_UPDATE_ERROR_DB.description, e.pgcode, e.pgerror)
            error_code = VPNCError.VPNSERVER_UPDATE_ERROR_DB.value
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        self._version = updated[self._version_field]
        self._state_version = updated[self._state_version_field]

    def __map_vpnserverdb_to_vpnserver(self, vpnserver_db):
        return VPNServer(suuid=vpnserver_db[self._suuid_field], version=vpnserver_db[self._version_field],
                         state_version=vpnserver_db[self._state_version_field],
                         type_id=vpnserver_db[self._type_id_field], status_id=vpnserver_db[self._status_id_field],
                         bandwidth=vpnserver_db[self._bandwidth_field], load=vpnserver_db[self._load_field],
                         geo_position_id=vpnserver_db[self._geo_position_id_field],
                         created_date=vpnserver_db[self._created_date_field])
