import logging
import sys
import uuid

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class VPNServerConfiguration(object):
    __version__ = 1

    _suuid = None
    _user_uuid = None
    _server_uuid = None
    _file_path = None
    _configuration = None
    _version = None

    def __init__(self, suuid: str = None, user_uuid: str = None, server_uuid: str = None, file_path: str = None,
                 configuration: str = None, version: int = None):
        self._suuid = suuid
        self._user_uuid = user_uuid
        self._server_uuid = server_uuid
        self._file_path = file_path
        self._configuration = configuration
        self._version = version

    def to_dict(self):
        return {
            'uuid': self._suuid,
            'user_uuid': self._user_uuid,
            'server_uuid': self._server_uuid,
            'file_path': self._file_path,
            'configuration': self._configuration,
            'version': self._version,
        }

    def to_api_dict(self):
        return {
            'uuid': str(self._suuid),
            'user_uuid': str(self._user_uuid),
            'server_uuid': str(self._server_uuid),
            'configuration': self._configuration,
            'version': self._version,
        }


class VPNServerConfigurationStored(StoredObject, VPNServerConfiguration):
    __version__ = 1

    def __init__(self, storage_service: StorageService, suuid: str = None, user_uuid: str = None,
                 server_uuid: str = None, file_path: str = None, configuration: str = None, version: int = None,
                 limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        VPNServerConfiguration.__init__(self, suuid=suuid, user_uuid=user_uuid, server_uuid=server_uuid,
                                        file_path=file_path, configuration=configuration, version=version)


class VPNServerConfigurationDB(VPNServerConfigurationStored):
    __version__ = 1

    _suuid_field = 'uuid'
    _user_uuid_field = 'user_uuid'
    _server_uuid_field = 'server_uuid'
    _file_path_field = 'file_path'
    _configuration_field = 'configuration'
    _version_field = 'version'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('VPNServerConfigurationDB find method')
        select_sql = '''
                      SELECT 
                        uuid,
                        user_uuid,
                        server_uuid,
                        file_path,
                        configuration,
                        version,
                        to_json(created_date) AS created_date 
                      FROM public.vpnserver_configuration
                      '''
        if self._limit:
            select_sql += "\nLIMIT %s\nOFFSET %s" % (self._limit, self._offset)
        logging.debug('Select SQL: %s' % select_sql)

        try:
            logging.debug('Call database service')
            vpnserverconfig_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = VPNCError.VPNSERVERCONFIG_FIND_ERROR_DB.message
            error_code = VPNCError.VPNSERVERCONFIG_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONFIG_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        vpnserverconfig_list = []

        for vpnserverconfig_db in vpnserverconfig_list_db:
            vpnserverconfig = self.__map_vpnserverconfigdb_to_vpnserverconfig(vpnserverconfig_db)
            vpnserverconfig_list.append(vpnserverconfig)

        if len(vpnserverconfig_list) == 0:
            logging.warning('Empty VPNServers list of method find_all. Very strange behaviour.')

        return vpnserverconfig_list

    def find_by_suuid(self):
        logging.info('VPNServerConfigurationDB find_by_server_uuid method')
        select_sql = '''
                      SELECT 
                        uuid,
                        user_uuid,
                        server_uuid,
                        file_path,
                        configuration,
                        version,
                        to_json(created_date) AS created_date 
                      FROM public.vpnserver_configuration
                      WHERE uuid = ?
                      '''
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
            error_message = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB.message
            error_code = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(vpnserver_configuration_list_db) == 1:
            vpnserver_db = vpnserver_configuration_list_db[0]
        elif len(vpnserver_configuration_list_db) == 0:
            error_message = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR.message
            error_code = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR.code
            developer_message = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR.developer_message
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR.developer_message
            error_code = VPNCError.VPNSERVERCONFIG_FIND_BY_UUID_ERROR.code
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_vpnserverconfigdb_to_vpnserverconfig(vpnserver_db)

    def find_by_server_uuid(self):
        logging.info('VPNServerConfigurationDB find_by_server_uuid method')
        select_sql = '''
                      SELECT 
                        uuid,
                        user_uuid,
                        server_uuid,
                        file_path,
                        configuration,
                        version,
                        to_json(created_date) AS created_date 
                      FROM public.vpnserver_configuration
                      WHERE server_uuid = ?
                      '''
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._server_uuid,)

        try:
            logging.debug('Call database service')
            vpnserver_configuration_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR_DB.message
            error_code = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR_DB.developer_message,
                                    e.pgcode, e.pgerror
                                )
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(vpnserver_configuration_list_db) == 1:
            vpnserver_db = vpnserver_configuration_list_db[0]
        elif len(vpnserver_configuration_list_db) == 0:
            error_message = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR.message
            error_code = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR.code
            developer_message = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR.developer_message
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." \
                                % VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR.developer_message
            error_code = VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR.code
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_vpnserverconfigdb_to_vpnserverconfig(vpnserver_db)

    def find_user_config(self):
        logging.info('VPNServerConfigurationDB find_user_config method')
        select_sql = '''
                      SELECT 
                        uuid,
                        user_uuid,
                        server_uuid,
                        file_path,
                        configuration,
                        version,
                        to_json(created_date) AS created_date 
                      FROM public.vpnserver_configuration
                      WHERE server_uuid = ? AND user_uuid = ?
                      '''
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._server_uuid, self._user_uuid)

        try:
            logging.debug('Call database service')
            vpnserver_configuration_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR_DB.message
            error_code = VPNCError.VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONFIG_FIND_BY_SERVER_UUID_ERROR_DB.developer_message,
                                    e.pgcode, e.pgerror
                                )
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(vpnserver_configuration_list_db) == 1:
            vpnserver_db = vpnserver_configuration_list_db[0]
        elif len(vpnserver_configuration_list_db) == 0:
            error_message = VPNCError.VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR.message
            error_code = VPNCError.VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR.code
            developer_message = VPNCError.VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR.developer_message
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = VPNCError.VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." \
                                % VPNCError.VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR.developer_message
            error_code = VPNCError.VPNSERVERCONFIG_FIND_USER_CONFIG_ERROR.code
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_vpnserverconfigdb_to_vpnserverconfig(vpnserver_db)

    def create(self):
        logging.info('VPNServerConfiguration create method')
        self._suuid = uuid.uuid4()
        logging.info('Create object VPNServerConfiguration with uuid: ' + str(self._suuid))
        insert_sql = '''
                      INSERT INTO public.vpnserver_configuration 
                        (uuid, server_uuid, user_uuid, file_path, configuration) 
                      VALUES 
                        (?, ?, ?, ?, ?)
                     '''
        insert_params = (
            self._suuid,
            self._server_uuid,
            self._user_uuid,
            self._file_path,
            self._configuration,
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
            error_message = VPNCError.VPNSERVER_CREATE_ERROR_DB.message
            error_code = VPNCError.VPNSERVER_CREATE_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONFIG_CREATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)

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
                        file_path = ?,
                        configuration = ?,
                        version = version + 1
                    WHERE 
                      uuid = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._server_uuid,
            self._user_uuid,
            self._file_path,
            self._configuration,
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
            error_message = VPNCError.VPNSERVERCONFIG_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONFIG_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = VPNCError.VPNSERVERCONFIG_UPDATE_ERROR_DB.code
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

    def __map_vpnserverconfigdb_to_vpnserverconfig(self, vpnserverconfig_db):
        return VPNServerConfiguration(
            suuid=vpnserverconfig_db[self._suuid_field], user_uuid=vpnserverconfig_db[self._user_uuid_field],
            server_uuid=vpnserverconfig_db[self._server_uuid_field],
            file_path=vpnserverconfig_db[self._file_path_field],
            configuration=vpnserverconfig_db[self._configuration_field],
            version=vpnserverconfig_db[self._version_field],
        )
