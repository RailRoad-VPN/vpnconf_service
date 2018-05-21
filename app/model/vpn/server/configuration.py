import datetime
import logging
import sys
import uuid

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService

class VPNServerConfiguration(object):
    __version__ = 1

    _suuid = None
    _user_suuid = None
    _server_suuid = None
    _file_path = None

    def __init__(self, suuid: str = None, user_suuid: str = None, server_suuid: str = None, file_path: str = None):
        self._suuid = suuid
        self._user_suuid = user_suuid
        self._server_suuid = server_suuid
        self._file_path = file_path

    def to_dict(self):
        return {
            'suuid': self._suuid,
            'user_suuid': self._user_suuid,
            'server_suuid': self._server_suuid,
            'file_path': self._file_path,
        }


class VPNServerConfigurationStored(VPNServerConfiguration):
    __version__ = 1

    _storage_service = None

    def __init__(self, storage_service: StorageService, **kwargs: dict) -> None:
        super().__init__(**kwargs)

        self._storage_service = storage_service


class VPNServerConfigurationDB(VPNServerConfigurationStored):
    __version__ = 1

    _suuid_field = 'uuid'
    _user_suuid_field = 'user_uuid'
    _server_suuid_field = 'server_uuid'
    _file_path_field = 'file_path'

    def __init__(self, storage_service: StorageService, **kwargs: dict):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('VPNServerConfigurationDB find method')
        select_sql = 'SELECT * FROM public.vpnserver_configuration'
        logging.debug('Select SQL: %s' % select_sql)

        try:
            logging.debug('Call database service')
            vpnserverconfig_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = VPNCError.VPNSERVERCONFIG_FIND_ERROR_DB.phrase
            error_code = VPNCError.VPNSERVERCONFIG_FIND_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONFIG_FIND_ERROR_DB.description, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        vpnserverconfig_list = []

        for vpnserverconfig_db in vpnserverconfig_list_db:
            vpnserverconfig = self.__map_vpnserverconfigdb_to_vpnserverconfig(vpnserverconfig_db)
            vpnserverconfig_list.append(vpnserverconfig)

        if len(vpnserverconfig_list) == 0:
            logging.warning('Empty VPNServers list of method find_all. Very strange behaviour.')

        return vpnserverconfig_list

    def find_by_suuid(self):
        logging.info('VPNServerConfigurationDB find_by_server_suuid method')
        select_sql = 'SELECT * FROM public.vpnserver_configuration WHERE uuid = ?'
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._suuid,)

        try:
            logging.debug('Call database service')
            vpnserver_configuration_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB.phrase
            error_code = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB.description, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(vpnserver_configuration_list_db) == 1:
            vpnserver_db = vpnserver_configuration_list_db[0]
        elif len(vpnserver_configuration_list_db) == 0:
            error_message = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR.phrase
            error_code = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR.value
            developer_message = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR.description
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR.phrase
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR.description
            error_code = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR.value
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_vpnserverconfigdb_to_vpnserverconfig(vpnserver_db)

    def find_by_server_suuid(self):
        logging.info('VPNServerConfigurationDB find_by_server_suuid method')
        select_sql = 'SELECT * FROM public.vpnserver_configuration WHERE server_uuid = ?'
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._suuid,)

        try:
            logging.debug('Call database service')
            vpnserver_configuration_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR_DB.phrase
            error_code = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR_DB.description,
                                    e.pgcode, e.pgerror
                                )
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(vpnserver_configuration_list_db) == 1:
            vpnserver_db = vpnserver_configuration_list_db[0]
        elif len(vpnserver_configuration_list_db) == 0:
            error_message = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR.phrase
            error_code = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR.value
            developer_message = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR.description
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR.phrase
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." \
                                % VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR.description
            error_code = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR.value
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_vpnserverconfigdb_to_vpnserverconfig(vpnserver_db)

    def create(self):
        logging.info('VPNServerConfiguration create method')
        self._suuid = uuid.uuid4()
        logging.info('Create object VPNServerConfiguration with uuid: ' + str(self._suuid))
        insert_sql = '''
                      INSERT INTO public.vpnserver_configuration 
                        (uuid, server_uuid, user_uuid, file_path) 
                      VALUES 
                        (?, ?, ?, ?)
                     '''
        insert_params = (
            self._suuid,
            self._server_suuid,
            self._user_suuid,
            self._file_path,
        )
        logging.debug('Create VPNServerConfiguration SQL : %s' % insert_sql)

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
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONFIG_CREATE_ERROR_DB.description, e.pgcode, e.pgerror)

            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('VPNServerConfiguration created.')

        return self._suuid

    def update(self):
        logging.info('VPNServerConfiguration update method')

        update_sql = '''
                    UPDATE public.vpnserver_configuration 
                    SET
                        server_uuid = ?, 
                        user_uuid = ?, 
                        file_path = ?
                    WHERE 
                      uuid = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._server_suuid,
            self._user_suuid,
            self._file_path,
            self._suuid,
        )

        try:
            logging.debug("Call database service")
            self._storage_service.update(sql=update_sql, data=update_params)
            logging.debug('VPNServerConfiguration updated.')
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVERCONFIG_UPDATE_ERROR_DB.phrase
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONFIG_UPDATE_ERROR_DB.description, e.pgcode, e.pgerror)
            error_code = VPNCError.VPNSERVERCONFIG_UPDATE_ERROR_DB.value
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

    def __map_vpnserverconfigdb_to_vpnserverconfig(self, vpnserverconfig_db):
        return VPNServerConfiguration(
            suuid=vpnserverconfig_db[self._suuid_field], user_suuid=vpnserverconfig_db[self._user_suuid_field],
            server_suuid=vpnserverconfig_db[self._server_suuid_field],
            file_path=vpnserverconfig_db[self._file_path_field],
        )

    @property
    def suuid_field(self):
        return type(self)._suuid_field

    @property
    def user_suuid_field(self):
        return type(self)._user_suuid_field

    @property
    def server_suuid_field(self):
        return type(self)._server_suuid_field

    @property
    def file_path_field(self):
        return type(self)._file_path_field