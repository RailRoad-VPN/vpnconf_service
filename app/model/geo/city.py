import datetime
import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import VPNException, VPNCError, VPNNotFoundException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class City(object):
    __version__ = 1

    _sid = None
    _name = None
    _created_date = None

    def __init__(self, sid: int = None, name: str = None, created_date: datetime = None):
        self._sid = sid
        self._name = name
        self._created_date = created_date

    def to_dict(self):
        return {
            'id': self._sid,
            'name': self._name,
            'created_date': self._created_date,
        }

    def to_api_dict(self):
        return {
            'id': self._sid,
            'name': self._name,
        }


class CityStored(StoredObject, City):
    __version__ = 1

    def __init__(self, storage_service: StorageService, sid: int = None, name: str = None,
                 created_date: datetime = None, limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        City.__init__(self, sid=sid, name=name, created_date=created_date)


class CityDB(CityStored):
    __version__ = 1

    _sid_field = 'id'
    _name_field = 'name'
    _created_date_field = 'created_date'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def find(self):
        logging.info('CityDB find method')
        select_sql = '''
                      SELECT 
                        id,
                        name,
                        to_json(created_date) AS created_date 
                      FROM public.city
                      '''
        if self._limit:
            select_sql += "\nLIMIT %s\nOFFSET %s" % (self._limit, self._offset)
        logging.debug(f"Select SQL: {select_sql}")

        try:
            logging.debug('Call database service')
            city_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = VPNCError.CITY_FIND_ERROR_DB.message
            error_code = VPNCError.CITY_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.CITY_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        city_list = []

        for city_db in city_list_db:
            vpnserverconfig = self.__map_citydb_to_city(city_db)
            city_list.append(vpnserverconfig)

        if len(city_list) == 0:
            logging.warning('Empty VPNServers list of method find_all. Very strange behaviour.')

        return city_list

    def find_by_sid(self):
        logging.info('CityDB find_by_server_uuid method')
        select_sql = '''
                      SELECT 
                        id,
                        name,
                        to_json(created_date) AS created_date 
                      FROM public.city
                      WHERE id = ?
                      '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (self._sid,)

        try:
            logging.debug('Call database service')
            city_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.CITY_FIND_BY_UUID_ERROR_DB.message
            error_code = VPNCError.CITY_FIND_BY_UUID_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.CITY_FIND_BY_UUID_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(city_list_db) == 1:
            vpnserver_db = city_list_db[0]
        elif len(city_list_db) == 0:
            error_message = VPNCError.CITY_FIND_BY_UUID_ERROR.message
            error_code = VPNCError.CITY_FIND_BY_UUID_ERROR.code
            developer_message = VPNCError.CITY_FIND_BY_UUID_ERROR.developer_message
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = VPNCError.CITY_FIND_BY_UUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % VPNCError.CITY_FIND_BY_UUID_ERROR.developer_message
            error_code = VPNCError.CITY_FIND_BY_UUID_ERROR.code
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_citydb_to_city(vpnserver_db)

    def create(self):
        logging.info('CityDB create method')
        insert_sql = '''
                      INSERT INTO public.city 
                        (name) 
                      VALUES 
                        (?)
                     '''
        insert_params = (
            self._name,
        )
        logging.debug('Create CityDB SQL : %s' % insert_sql)

        try:
            logging.debug('Call database service')
            data = self._storage_service.create(sql=insert_sql, data=insert_params, is_return=True)
            self._sid = data[self._sid_field]
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.CITY_CREATE_ERROR_DB.message
            error_code = VPNCError.CITY_CREATE_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.CITY_CREATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)

            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('CityDB created.')

        return self._sid

    def update(self):
        logging.info('City update method')

        update_sql = '''
                    UPDATE public.city 
                    SET
                        name = ?
                    WHERE 
                        id = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._name,
            self._sid,
        )

        try:
            logging.debug("Call database service")
            self._storage_service.update(sql=update_sql, data=update_params)
            logging.debug('City updated.')
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.CITY_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.CITY_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = VPNCError.CITY_UPDATE_ERROR_DB.code
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

    def __map_citydb_to_city(self, city_db):
        return City(
            sid=city_db[self._sid_field],
            name=city_db[self._name_field],
            created_date=city_db[self._created_date_field],
        )
