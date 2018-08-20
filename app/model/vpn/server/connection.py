import datetime
import logging
import uuid

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class VPNServerConnection(object):
    __version__ = 1

    suuid = None
    server_uuid = None
    user_uuid = None
    user_device_uuid = None
    device_ip = None
    virtual_ip = None
    bytes_i = None
    bytes_o = None
    is_connected = None
    connected_since = None
    created_date = None

    def __init__(self, suuid: str = None, server_uuid: str = None, user_uuid: str = None, user_device_uuid: str = None,
                 device_ip: str = None, virtual_ip: str = None, bytes_i: float = None, bytes_o: float = None,
                 is_connected: str = None, connected_since: datetime = None, created_date: datetime = None):
        self._suuid = suuid
        self._server_uuid = server_uuid
        self._user_uuid = user_uuid
        self._user_device_uuid = user_device_uuid
        self._device_ip = device_ip
        self._virtual_ip = virtual_ip
        self._bytes_i = bytes_i
        self._bytes_o = bytes_o
        self._is_connected = is_connected
        self._connected_since = connected_since
        self._created_date = created_date

    def to_dict(self):
        return {
            'uuid': self._suuid,
            'server_uuid': self._server_uuid,
            'user_uuid': self._user_uuid,
            'user_device_uuid': self._user_device_uuid,
            'device_ip': self._device_ip,
            'virtual_ip': self._virtual_ip,
            'bytes_i': self._bytes_i,
            'bytes_o': self._bytes_o,
            'is_connected': self._is_connected,
            'connected_since': self._connected_since,
            'created_date': self._created_date,
        }

    def to_api_dict(self):
        return {
            'uuid': str(self._suuid),
            'server_uuid': str(self._server_uuid),
            'user_uuid': str(self._user_uuid),
            'user_device_uuid': self._user_device_uuid,
            'device_ip': self._device_ip,
            'virtual_ip': self._virtual_ip,
            'bytes_i': self._bytes_i,
            'bytes_o': self._bytes_o,
            'is_connected': self._is_connected,
            'connected_since': self._connected_since,
            'created_date': self._created_date,
        }


class VPNServerConnectionStored(StoredObject, VPNServerConnection):
    __version__ = 1

    def __init__(self, storage_service: StorageService, suuid: str = None, server_uuid: str = None,
                 user_uuid: str = None, device_ip: str = None, virtual_ip: str = None, bytes_i: float = None,
                 bytes_o: float = None, is_connected: str = None, connected_since: datetime = None,
                 created_date: datetime = None, limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        VPNServerConnection.__init__(self, suuid=suuid, server_uuid=server_uuid, user_uuid=user_uuid,
                                     device_ip=device_ip, virtual_ip=virtual_ip, bytes_i=bytes_i, bytes_o=bytes_o,
                                     is_connected=is_connected, connected_since=connected_since,
                                     created_date=created_date)


class VPNServerConnectionDB(VPNServerConnectionStored):
    __version__ = 1

    _suuid_field = 'uuid'
    _server_uuid_field = 'server_uuid'
    _user_uuid_field = 'user_uuid'
    _user_device_uuid_field = 'user_device_uuid'
    _device_ip_field = 'device_ip'
    _virtual_ip_field = 'virtual_ip'
    _bytes_i_field = 'bytes_i'
    _bytes_o_field = 'bytes_o'
    _is_connected_field = 'is_connected'
    _connected_since_field = 'connected_since'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('VPNServerConnectionDB find method')
        select_sql = '''
                      SELECT 
                        uuid,
                        server_uuid,
                        user_uuid,
                        user_device_uuid,
                        device_ip,
                        virtual_ip,
                        bytes_i,
                        bytes_o,
                        is_connected,
                        to_json(connected_since) AS connected_since,
                        to_json(created_date) AS created_date 
                      FROM public.vpnserver_connection
                      '''
        if self._limit:
            select_sql += f"\nLIMIT {self._limit}\nOFFSET {self._offset}"
        logging.debug(f"Select SQL: {select_sql}")

        try:
            logging.debug('Call database service')
            vpnserverconn_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = VPNCError.VPNSERVERCONN_FIND_ERROR_DB.message
            error_code = VPNCError.VPNSERVERCONN_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONN_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        vpnserverconn_list = []

        for vpnserverconn_db in vpnserverconn_list_db:
            vpnserverconn = self.__map_vpnserverconndb_to_vpnserverconn(vpnserverconn_db)
            vpnserverconn_list.append(vpnserverconn)

        if len(vpnserverconn_list) == 0:
            logging.warning('Empty VPNServers list of method find_all. Very strange behaviour.')

        return vpnserverconn_list

    def find_by_suuid(self):
        logging.info('VPNServerConnectionDB find_by_suuid method')
        select_sql = '''
                      SELECT 
                        uuid,
                        server_uuid,
                        user_uuid,
                        user_device_uuid,
                        device_ip,
                        virtual_ip,
                        bytes_i,
                        bytes_o,
                        is_connected,
                        to_json(connected_since) AS connected_since,
                        to_json(created_date) AS created_date 
                      FROM public.vpnserver_connection
                      WHERE uuid = ?
                      '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (self._suuid,)

        try:
            logging.debug('Call database service')
            vpnserver_connection_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVERCONN_FIND_BY_UUID_ERROR_DB.message
            error_code = VPNCError.VPNSERVERCONN_FIND_BY_UUID_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONN_FIND_BY_UUID_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(vpnserver_connection_list_db) == 1:
            vpnserver_conn_db = vpnserver_connection_list_db[0]
        elif len(vpnserver_connection_list_db) == 0:
            error_message = VPNCError.VPNSERVERCONN_FIND_BY_UUID_ERROR.message
            error_code = VPNCError.VPNSERVERCONN_FIND_BY_UUID_ERROR.code
            developer_message = VPNCError.VPNSERVERCONN_FIND_BY_UUID_ERROR.developer_message
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = VPNCError.VPNSERVERCONN_FIND_BY_UUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % VPNCError.VPNSERVERCONN_FIND_BY_UUID_ERROR.developer_message
            error_code = VPNCError.VPNSERVERCONN_FIND_BY_UUID_ERROR.code
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_vpnserverconndb_to_vpnserverconn(vpnserver_conn_db)

    def find_by_server_uuid(self):
        logging.info('VPNServerConnectionDB find_by_server_uuid method')
        select_sql = '''
                      SELECT 
                        uuid,
                        server_uuid,
                        user_uuid,
                        user_device_uuid,
                        device_ip,
                        virtual_ip,
                        bytes_i,
                        bytes_o,
                        is_connected,
                        to_json(connected_since) AS connected_since,
                        to_json(created_date) AS created_date 
                      FROM public.vpnserver_connection
                      WHERE server_uuid = ?
                      '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (self._server_uuid,)

        try:
            logging.debug('Call database service')
            vpnserverconn_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVERCONN_FIND_BY_SERVER_UUID_ERROR_DB.message
            error_code = VPNCError.VPNSERVERCONN_FIND_BY_SERVER_UUID_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONN_FIND_BY_SERVER_UUID_ERROR_DB.developer_message,
                                    e.pgcode, e.pgerror
                                )
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        vpnserverconn_list = []

        for vpnserverconn_db in vpnserverconn_list_db:
            vpnserverconn = self.__map_vpnserverconndb_to_vpnserverconn(vpnserverconn_db)
            vpnserverconn_list.append(vpnserverconn)

        return vpnserverconn_list

    def find_by_server_and_user(self):
        logging.info('VPNServerConnectionDB find_by_server_and_user method')
        select_sql = '''
                      SELECT 
                        uuid,
                        server_uuid,
                        user_uuid,
                        user_device_uuid,
                        device_ip,
                        virtual_ip,
                        bytes_i,
                        bytes_o,
                        is_connected,
                        to_json(connected_since) AS connected_since,
                        to_json(created_date) AS created_date 
                      FROM public.vpnserver_connection
                      WHERE server_uuid = ? AND user_uuid = ?
                      '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (self._server_uuid, self._user_uuid)

        try:
            logging.debug('Call database service')
            vpnserver_connection_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVERCONN_FIND_USER_CONN_ERROR_DB.message
            error_code = VPNCError.VPNSERVERCONN_FIND_USER_CONN_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONN_FIND_BY_SERVER_UUID_ERROR_DB.developer_message,
                                    e.pgcode, e.pgerror
                                )
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        vpnserverconn_list = []

        for vpnserverconn_db in vpnserver_connection_list_db:
            vpnserverconn = self.__map_vpnserverconndb_to_vpnserverconn(vpnserverconn_db)
            vpnserverconn_list.append(vpnserverconn)

        return vpnserverconn_list

    def find_by_server_and_user_device(self):
        logging.info('VPNServerConnectionDB find_by_server_and_user_device method')
        select_sql = '''
                      SELECT 
                        uuid,
                        server_uuid,
                        user_uuid,
                        user_device_uuid,
                        device_ip,
                        virtual_ip,
                        bytes_i,
                        bytes_o,
                        is_connected,
                        to_json(connected_since) AS connected_since,
                        to_json(created_date) AS created_date 
                      FROM public.vpnserver_connection vc
                      WHERE server_uuid = ? AND user_device_uuid = ?
                      ORDER BY vc.created_date DESC
                      '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (
            self._server_uuid,
            self._user_device_uuid,
        )

        try:
            logging.debug('Call database service')
            vpnserver_connection_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVERCONN_FIND_BY_SERVER_AND_USER_DEVICE_ERROR_DB.message
            error_code = VPNCError.VPNSERVERCONN_FIND_BY_SERVER_AND_USER_DEVICE_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONN_FIND_BY_SERVER_AND_USER_DEVICE_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(vpnserver_connection_list_db) > 0:
            vpnserver_conn_db = vpnserver_connection_list_db[0]
        else:
            error_message = VPNCError.VPNSERVERCONN_FIND_BY_SERVER_AND_USER_DEVICE_ERROR.message
            error_code = VPNCError.VPNSERVERCONN_FIND_BY_SERVER_AND_USER_DEVICE_ERROR.code
            developer_message = VPNCError.VPNSERVERCONN_FIND_BY_SERVER_AND_USER_DEVICE_ERROR.developer_message
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_vpnserverconndb_to_vpnserverconn(vpnserver_conn_db)

    def find_by_server_and_virtual_ip(self):
        logging.info('VPNServerConnectionDB find_by_server_and_virtual_ip method')
        select_sql = '''
                      SELECT 
                        uuid,
                        server_uuid,
                        user_uuid,
                        user_device_uuid,
                        device_ip,
                        virtual_ip,
                        bytes_i,
                        bytes_o,
                        is_connected,
                        to_json(connected_since) AS connected_since,
                        to_json(created_date) AS created_date 
                      FROM public.vpnserver_connection vc
                      WHERE server_uuid = ? AND virtual_ip = ?
                      ORDER BY vc.created_date DESC
                      '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (
            self._server_uuid,
            self._virtual_ip,
        )

        try:
            logging.debug('Call database service')
            vpnserver_connection_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVERCONN_FIND_BY_SERVER_AND_VIRTUAL_IP_ERROR_DB.message
            error_code = VPNCError.VPNSERVERCONN_FIND_BY_SERVER_AND_VIRTUAL_IP_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONN_FIND_BY_SERVER_AND_VIRTUAL_IP_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(vpnserver_connection_list_db) > 0:
            vpnserver_conn_db = vpnserver_connection_list_db[0]
        else:
            error_message = VPNCError.VPNSERVERCONN_FIND_BY_SERVER_AND_VIRTUAL_IP_ERROR.message
            error_code = VPNCError.VPNSERVERCONN_FIND_BY_SERVER_AND_VIRTUAL_IP_ERROR.code
            developer_message = VPNCError.VPNSERVERCONN_FIND_BY_SERVER_AND_VIRTUAL_IP_ERROR.developer_message
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_vpnserverconndb_to_vpnserverconn(vpnserver_conn_db)

    def create(self):
        logging.info('VPNServerConnection create method')
        self._suuid = uuid.uuid4()
        logging.info('Create object VPNServerConnection with uuid: ' + str(self._suuid))
        insert_sql = '''
                      INSERT INTO public.vpnserver_connection 
                        (uuid, server_uuid, user_uuid, user_device_uuid, device_ip, virtual_ip, bytes_i, bytes_o, is_connected, 
                        connected_since, created_date) 
                      VALUES 
                        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                     '''
        insert_params = (
            self._suuid,
            self._server_uuid,
            self._user_uuid,
            self._user_device_uuid,
            self._device_ip,
            self._virtual_ip,
            self._bytes_i,
            self._bytes_o,
            self._is_connected,
            self._connected_since,
            self._created_date,
        )
        logging.debug('Create VPNServerConnection SQL : %s' % insert_sql)

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
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONN_CREATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)

            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('VPNServerConnection created.')

        return self._suuid

    def update(self):
        logging.info('VPNServerConnection update method')

        update_sql = '''
                    UPDATE public.vpnserver_connection 
                    SET
                        server_uuid = ?,
                        user_uuid = ?,
                        user_device_uuid = ?,
                        device_ip = ?,
                        virtual_ip = ?,
                        bytes_i = ?,
                        bytes_o = ?,
                        is_connected = ?,
                        connected_since = ?
                    WHERE 
                      uuid = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._server_uuid,
            self._user_uuid,
            self._user_device_uuid,
            self._device_ip,
            self._virtual_ip,
            self._bytes_i,
            self._bytes_o,
            self._is_connected,
            self._connected_since,
            self._suuid,
        )

        try:
            logging.debug("Call database service")
            self._storage_service.update(sql=update_sql, data=update_params)
            logging.debug('VPNServerConnection updated.')
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVERCONN_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVERCONN_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = VPNCError.VPNSERVERCONN_UPDATE_ERROR_DB.code
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

    def __map_vpnserverconndb_to_vpnserverconn(self, vpnserverconn_db):
        return VPNServerConnection(
            suuid=vpnserverconn_db[self._suuid_field],
            user_uuid=vpnserverconn_db[self._user_uuid_field],
            server_uuid=vpnserverconn_db[self._server_uuid_field],
            user_device_uuid=vpnserverconn_db[self._user_device_uuid_field],
            device_ip=vpnserverconn_db[self._device_ip_field],
            virtual_ip=vpnserverconn_db[self._virtual_ip_field],
            bytes_i=vpnserverconn_db[self._bytes_i_field],
            bytes_o=vpnserverconn_db[self._bytes_o_field],
            is_connected=vpnserverconn_db[self._is_connected_field],
            connected_since=vpnserverconn_db[self._connected_since_field],
            created_date=vpnserverconn_db[self._created_date_field],
        )
