import datetime
import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import VPNException, VPNCError, VPNNotFoundException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService


class Geo(object):
    __version__ = 1

    _sid = None
    _latitude = None
    _longitude = None
    _country_code = None
    _state_code = None
    _city_id = None
    _region_common = None
    _region_dvd = None
    _region_xbox360 = None
    _region_xboxone = None
    _region_playstation3 = None
    _region_playstation4 = None
    _region_nintendo = None
    _created_date = None

    def __init__(self, sid: int = None, latitude: str = None, longitude: str = None, country_code: str = None,
                 state_code: str = None, city_id: int = None, region_common: int = None, region_dvd: int = None,
                 region_xbox360: int = None, region_xboxone: int = None, region_playstation3: int = None,
                 region_playstation4: int = None, region_nintendo: int = None, created_date: datetime = None):
        self._sid = sid
        self._latitude = latitude
        self._longitude = longitude
        self._country_code = country_code
        self._state_code = state_code
        self._city_id = city_id
        self._region_common = region_common
        self._region_dvd = region_dvd
        self._region_xbox360 = region_xbox360
        self._region_xboxone = region_xboxone
        self._region_playstation3 = region_playstation3
        self._region_playstation4 = region_playstation4
        self._region_nintendo = region_nintendo
        self._created_date = created_date

    def to_dict(self):
        return {
            'sid': self._sid,
            'latitude': self._latitude,
            'longitude': self._longitude,
            'country_code': self._country_code,
            'state_code': self._state_code,
            'city_id': self._city_id,
            'region_common': self._region_common,
            'region_dvd': self._region_dvd,
            'region_xbox360': self._region_xbox360,
            'region_xboxone': self._region_xboxone,
            'region_playstation3': self._region_playstation3,
            'region_playstation4': self._region_playstation4,
            'region_nintendo': self._region_nintendo,
            'created_date': self._created_date,
        }


class GeoStored(Geo):
    __version__ = 1

    _storage_service = None

    def __init__(self, storage_service: StorageService, **kwargs: dict) -> None:
        super().__init__(**kwargs)

        self._storage_service = storage_service


class GeoDB(GeoStored):
    __version__ = 1

    _sid_field = 'id'
    _latitude_field = 'latitude'
    _longitude_field = 'longitude'
    _country_code_field = 'country_code'
    _state_code_field = 'state_code'
    _city_id_field = 'city_id'
    _region_common_field = 'region_common'
    _region_dvd_field = 'region_dvd'
    _region_xbox360_field = 'region_xbox360'
    _region_xboxone_field = 'region_xboxone'
    _region_playstation3_field = 'region_playstation3'
    _region_playstation4_field = 'region_playstation4'
    _region_nintendo_field = 'region_nintendo'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs: dict):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('GeoDB find method')
        select_sql = 'SELECT * FROM public.geo_position'
        logging.debug('Select SQL: %s' % select_sql)

        try:
            logging.debug('Call database service')
            geo_position_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = VPNCError.GEO_FIND_ERROR_DB.phrase
            error_code = VPNCError.GEO_FIND_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.GEO_FIND_ERROR_DB.description, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        geo_position_list = []

        for geo_position_db in geo_position_list_db:
            geo_position = self.__map_geodb_to_geo(geo_position_db)
            geo_position_list.append(geo_position)

        if len(geo_position_list) == 0:
            logging.warning('Empty Geo list of method find_all. Very strange behaviour.')

        return geo_position_list

    def find_by_id(self):
        logging.info('GeoDB find_by_id method')
        select_sql = 'SELECT * FROM public.geo_position WHERE id = ?'
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._sid,)

        try:
            logging.debug('Call database service')
            geo_position_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.GEO_FIND_BY_ID_ERROR_DB.phrase
            error_code = VPNCError.GEO_FIND_BY_ID_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.GEO_FIND_BY_ID_ERROR_DB.description, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(geo_position_list_db) == 1:
            geo_position_db = geo_position_list_db[0]
        elif len(geo_position_list_db) == 0:
            error_message = VPNCError.GEO_FIND_BY_ID_ERROR.phrase
            error_code = VPNCError.GEO_FIND_BY_ID_ERROR.value
            developer_message = VPNCError.GEO_FIND_BY_ID_ERROR.description
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = VPNCError.GEO_FIND_BY_ID_ERROR.phrase
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % VPNCError.GEO_FIND_BY_ID_ERROR.description
            error_code = VPNCError.GEO_FIND_BY_ID_ERROR.value
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_geodb_to_geo(geo_position_db)

    def create(self):
        logging.info('GeoDB create method')
        insert_sql = '''
                      INSERT INTO public.geo_position
                      (latitude, longitude, country_code, state_code, city_id, region_common, region_dvd, 
                      region_xbox360, region_xboxone, region_playstation3, region_playstation4, region_nintendo, 
                      created_date) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                     '''
        insert_params = (
            self._latitude,
            self._longitude,
            self._country_code,
            self._state_code,
            self._city_id,
            self._region_common,
            self._region_dvd,
            self._region_xbox360,
            self._region_xboxone,
            self._region_playstation3,
            self._region_playstation4,
            self._region_nintendo,
            self._created_date,
        )
        logging.debug('Create GeoDB SQL : %s' % insert_sql)

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
            error_message = VPNCError.GEO_CREATE_ERROR_DB.phrase
            error_code = VPNCError.GEO_CREATE_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.GEO_CREATE_ERROR_DB.description, e.pgcode, e.pgerror)

            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('GeoDB created.')

        return self._sid

    def update(self):
        logging.info('Geo update method')

        update_sql = '''
                    UPDATE public.geo_position 
                    SET
                        latitude = ?,
                        longitude = ?,
                        country_code = ?,
                        state_code = ?,
                        city_id = ?,
                        region_common = ?,
                        region_dvd = ?,
                        region_xbox360 = ?,
                        region_xboxone = ?,
                        region_playstation3 = ?,
                        region_playstation4 = ?,
                        region_nintendo = ?,
                    WHERE 
                        id = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._latitude,
            self._longitude,
            self._country_code,
            self._state_code,
            self._city_id,
            self._region_common,
            self._region_dvd,
            self._region_xbox360,
            self._region_xboxone,
            self._region_playstation3,
            self._region_playstation4,
            self._region_nintendo,
        )

        try:
            logging.debug("Call database service")
            self._storage_service.update(sql=update_sql, data=update_params)
            logging.debug('Geo updated.')
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.GEO_UPDATE_ERROR_DB.phrase
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.GEO_UPDATE_ERROR_DB.description, e.pgcode, e.pgerror)
            error_code = VPNCError.GEO_UPDATE_ERROR_DB.value
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

    def __map_geodb_to_geo(self, geo_position_db):
        return Geo(
            sid=geo_position_db[self._sid_field],
            latitude=geo_position_db[self._latitude_field],
            longitude=geo_position_db[self._longitude_field],
            country_code=geo_position_db[self._country_code_field],
            state_code=geo_position_db[self._state_code_field],
            city_id=geo_position_db[self._city_id_field],
            region_common=geo_position_db[self._region_common_field],
            region_dvd=geo_position_db[self._region_dvd_field],
            region_xbox360=geo_position_db[self._region_xbox360_field],
            region_xboxone=geo_position_db[self._region_xboxone_field],
            region_playstation3=geo_position_db[self._region_playstation3_field],
            region_playstation4=geo_position_db[self._region_playstation4_field],
            region_nintendo=geo_position_db[self._region_nintendo_field],
            created_date=geo_position_db[self._created_date_field],
        )

    @property
    def _sid_field(self):
        return type(self)._sid_field

    @property
    def _latitude_field(self):
        return type(self)._latitude_field

    @property
    def _longitude_field(self):
        return type(self)._longitude_field

    @property
    def _country_code_field(self):
        return type(self)._country_code_field

    @property
    def _geo_position_code_field(self):
        return type(self)._geo_position_code_field

    @property
    def _city_id_field(self):
        return type(self)._city_id_field

    @property
    def _region_common_field(self):
        return type(self)._region_common_field

    @property
    def _region_dvd_field(self):
        return type(self)._region_dvd_field

    @property
    def _region_xbox360_field(self):
        return type(self)._region_xbox360_field

    @property
    def _region_xboxone_field(self):
        return type(self)._region_xboxone_field

    @property
    def _region_playstation3_field(self):
        return type(self)._region_playstation3_field

    @property
    def _region_playstation4_field(self):
        return type(self)._region_playstation4_field

    @property
    def _region_nintendo_field(self):
        return type(self)._region_nintendo_field

    @property
    def _created_date_field(self):
        return type(self)._created_date_field
