import datetime
import logging
import uuid

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class VPNServer(object):
    __version__ = 1

    _suuid = None
    _ip = None
    _hostname = None
    _version = None
    _condition_version = None
    _type_id = None
    _status_id = None
    _bandwidth = None
    _load = None
    _num = None
    _geo_position_id = None
    _created_date = None

    def __init__(self, suuid: str = None, ip: str = None, hostname: str = None, version: int = None,
                 condition_version: int = None, type_id: int = None,
                 status_id: int = None, bandwidth: int = None, load: int = None, num: int = None,
                 geo_position_id: int = None,
                 created_date: datetime = None):
        self._suuid = suuid
        self._ip = ip
        self._hostname = hostname
        self._version = version
        self._condition_version = condition_version
        self._type_id = type_id
        self._status_id = status_id
        self._bandwidth = bandwidth
        self._load = load
        self._num = num
        self._geo_position_id = geo_position_id
        self._created_date = created_date

    def to_api_dict(self):
        return {
            'uuid': str(self._suuid),
            'ip': self._ip,
            'hostname': self._hostname,
            'version': self._version,
            'condition_version': self._condition_version,
            'type_id': self._type_id,
            'status_id': self._status_id,
            'bandwidth': self._bandwidth,
            'load': self._load,
            'num': self._num,
            'geo_position_id': self._geo_position_id,
        }

    def to_dict(self):
        return {
            'uuid': str(self._suuid),
            'ip': self._ip,
            'hostname': self._hostname,
            'version': self._version,
            'condition_version': self._condition_version,
            'type_id': self._type_id,
            'status_id': self._status_id,
            'bandwidth': self._bandwidth,
            'load': self._load,
            'num': self._num,
            'geo_position_id': self._geo_position_id,
            'created_date': self._created_date,
        }


class VPNServerStored(StoredObject, VPNServer):
    __version__ = 1

    def __init__(self, storage_service: StorageService, suuid: str = None, ip: str = None, hostname: str = None,
                 version: int = None, condition_version: int = None, type_id: int = None, status_id: int = None,
                 bandwidth: int = None, load: int = None, num: int = None, geo_position_id: int = None,
                 created_date: datetime = None, limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        VPNServer.__init__(self, suuid=suuid, version=version, condition_version=condition_version, type_id=type_id,
                           status_id=status_id, bandwidth=bandwidth, load=load, num=num, ip=ip, hostname=hostname,
                           geo_position_id=geo_position_id, created_date=created_date)


class VPNServerDB(VPNServerStored):
    __version__ = 1

    _suuid_field = 'uuid'
    _ip_field = 'ip'
    _hostname_field = 'hostname'
    _version_field = 'version'
    _condition_version_field = 'condition_version'
    _type_id_field = 'type_id'
    _status_id_field = 'status_id'
    _bandwidth_field = 'bandwidth'
    _load_field = 'load'
    _num_field = 'num'
    _geo_position_id_field = 'geo_position_id'
    _created_date_field = 'created_date'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def find(self):
        self.logger.info('VPNServerDB find method')
        select_sql = '''
                      SELECT 
                          uuid, 
                          ip,
                          hostname,
                          version, 
                          condition_version, 
                          type_id, 
                          status_id, 
                          bandwidth, 
                          load, 
                          num, 
                          geo_position_id, 
                          to_json(created_date) AS created_date 
                      FROM public.vpnserver
                      ORDER BY num
                      '''
        if self._limit:
            select_sql += "\nLIMIT %s\nOFFSET %s" % (self._limit, self._offset)
        self.logger.debug(f"Select SQL: {select_sql}")

        try:
            self.logger.debug('Call database service')
            vpnserver_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = VPNCError.VPNSERVER_FIND_ERROR_DB.message
            error_code = VPNCError.VPNSERVER_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVER_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        vpnserver_list = []

        for vpnserver_db in vpnserver_list_db:
            vpnserver = self.__map_vpnserverdb_to_vpnserver(vpnserver_db)
            vpnserver_list.append(vpnserver)

        if len(vpnserver_list) == 0:
            logging.warning('Empty VPNServers list of method find_all. Very strange behaviour.')

        return vpnserver_list

    def find_by_suuid(self):
        self.logger.info('Find VPNServer by uuid')
        select_sql = '''
                      SELECT 
                          uuid, 
                          ip,
                          hostname,
                          version, 
                          condition_version, 
                          type_id, 
                          status_id, 
                          bandwidth, 
                          load, 
                          num,
                          geo_position_id, 
                          to_json(created_date) AS created_date 
                      FROM public.vpnserver 
                      WHERE uuid = ?
                      '''
        self.logger.debug(f"Select SQL: {select_sql}")
        params = (self._suuid,)

        try:
            self.logger.debug('Call database service')
            vpnserver_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR_DB.message
            error_code = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVER_FIND_BY_UUID_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(vpnserver_list_db) == 1:
            vpnserver_db = vpnserver_list_db[0]
        elif len(vpnserver_list_db) == 0:
            error_message = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR.message
            error_code = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR.code
            developer_message = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR.developer_message
            raise VPNNotFoundException(error=error_message, error_code=error_code,
                                       developer_message=developer_message)
        else:
            error_message = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % VPNCError.VPNSERVER_FIND_BY_UUID_ERROR.developer_message
            error_code = VPNCError.VPNSERVER_FIND_BY_UUID_ERROR.code
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_vpnserverdb_to_vpnserver(vpnserver_db)

    def find_by_status_id(self):
        self.logger.info('Find VPNServer by uuid')
        select_sql = '''
                      SELECT 
                          uuid, 
                          ip,
                          hostname,
                          version, 
                          condition_version, 
                          type_id, 
                          status_id, 
                          bandwidth, 
                          load, 
                          num,
                          geo_position_id, 
                          to_json(created_date) AS created_date 
                      FROM public.vpnserver 
                      WHERE status_id = ?
                      ORDER BY num
                      '''
        self.logger.debug(f"Select SQL: {select_sql}")
        params = (self._status_id,)

        try:
            self.logger.debug('Call database service')
            vpnserver_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVER_FIND_BY_STATUS_ID_DB.message
            error_code = VPNCError.VPNSERVER_FIND_BY_STATUS_ID_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVER_FIND_BY_STATUS_ID_DB.developer_message, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        vpnserver_list = []

        for vpnserver_db in vpnserver_list_db:
            vpnserver = self.__map_vpnserverdb_to_vpnserver(vpnserver_db)
            vpnserver_list.append(vpnserver)

        if len(vpnserver_list) == 0:
            logging.warning('Empty VPNServers list of method find by status id. Very strange behaviour.')

        return vpnserver_list

    def find_by_type_id(self):
        self.logger.info('Find VPNServer by uuid')
        select_sql = '''
                      SELECT 
                          uuid, 
                          ip,
                          hostname,
                          version, 
                          condition_version, 
                          type_id, 
                          status_id, 
                          bandwidth, 
                          load, 
                          num, 
                          geo_position_id, 
                          to_json(created_date) AS created_date 
                      FROM public.vpnserver 
                      WHERE type_id = ?
                      ORDER BY num
                      '''
        self.logger.debug(f"Select SQL: {select_sql}")
        params = (self._type_id,)

        try:
            self.logger.debug('Call database service')
            vpnserver_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVER_FIND_BY_TYPE_ID_DB.message
            error_code = VPNCError.VPNSERVER_FIND_BY_TYPE_ID_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVER_FIND_BY_TYPE_ID_DB.developer_message, e.pgcode, e.pgerror)
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
        self.logger.info('Create object VPNServer with uuid: ' + str(self._suuid))
        insert_sql = '''
                      INSERT INTO public.vpnserver 
                        (uuid, ip, hostname, type_id, status_id, bandwidth, geo_position_id, load) 
                      VALUES 
                        (?, ?, ?, ?, ?, ?, ?, ?)
                     '''
        insert_params = (
            self._suuid,
            self._ip,
            self._hostname,
            self._type_id,
            self._status_id,
            self._bandwidth,
            self._geo_position_id,
            self._load,
        )
        self.logger.debug('Create VPNServer SQL : %s' % insert_sql)

        try:
            self.logger.debug('Call database service')
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
                                    VPNCError.VPNSERVER_CREATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)

            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        self.logger.debug('VPNServer created.')

        return self._suuid

    def update(self):
        self.logger.info('Update VPNServer')

        update_sql = '''
                    UPDATE public.vpnserver 
                    SET ip = ?,
                        hostname = ?,
                        type_id = ?,
                        status_id = ?,
                        bandwidth = ?,
                        geo_position_id = ?,
                        load = ?
                    WHERE 
                      uuid = ?
                    RETURNING version, condition_version;
                    '''

        self.logger.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._ip,
            self._hostname,
            self._type_id,
            self._status_id,
            self._bandwidth,
            self._geo_position_id,
            self._load,
            self._suuid,
        )

        try:
            self.logger.debug("Call database service")
            updated = self._storage_service.update(sql=update_sql, data=update_params, is_return=True)
            updated = updated[0]
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVER_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVER_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = VPNCError.VPNSERVER_UPDATE_ERROR_DB.code
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        self._version = updated[self._version_field]
        self._condition_version = updated[self._condition_version_field]

    def __map_vpnserverdb_to_vpnserver(self, vpnserver_db):
        return VPNServer(suuid=vpnserver_db[self._suuid_field], version=vpnserver_db[self._version_field],
                         condition_version=vpnserver_db[self._condition_version_field],
                         ip=vpnserver_db[self._ip_field], hostname=vpnserver_db[self._hostname_field],
                         type_id=vpnserver_db[self._type_id_field], status_id=vpnserver_db[self._status_id_field],
                         bandwidth=vpnserver_db[self._bandwidth_field], load=vpnserver_db[self._load_field],
                         num=vpnserver_db[self._num_field], geo_position_id=vpnserver_db[self._geo_position_id_field],
                         created_date=vpnserver_db[self._created_date_field])
