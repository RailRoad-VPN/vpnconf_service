import datetime
import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import VPNException, VPNCError, VPNNotFoundException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService


class Country(object):
    __version__ = 1

    _code = None
    _str_code = None
    _name = None
    _created_date = None

    def __init__(self, code: int = None, str_code: str = None, name: str = None, created_date: datetime = None):
        self._code = code
        self._name = name
        self._str_code = str_code
        self._created_date = created_date

    def to_dict(self):
        return {
            'code': self._code,
            'name': self._name,
            'str_code': self._str_code,
            'created_date': self._created_date,
        }


class CountryStored(Country):
    __version__ = 1

    _storage_service = None

    def __init__(self, storage_service: StorageService, **kwargs) -> None:
        super().__init__(**kwargs)

        self._storage_service = storage_service


class CountryDB(CountryStored):
    __version__ = 1

    _code_field = 'code'
    _name_field = 'name'
    _str_code_field = 'str_code'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('CountryDB find method')
        select_sql = 'SELECT * FROM public.country'
        logging.debug('Select SQL: %s' % select_sql)

        try:
            logging.debug('Call database service')
            country_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = VPNCError.COUNTRY_FIND_ERROR_DB.phrase
            error_code = VPNCError.COUNTRY_FIND_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.COUNTRY_FIND_ERROR_DB.description, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        country_list = []

        for country_db in country_list_db:
            country = self.__map_countrydb_to_country(country_db)
            country_list.append(country)

        if len(country_list) == 0:
            logging.warning('Empty VPNServers list of method find_all. Very strange behaviour.')

        return country_list

    def find_by_code(self):
        logging.info('CountryDB find_by_code method')
        select_sql = 'SELECT * FROM public.country WHERE code = ?'
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._code,)

        try:
            logging.debug('Call database service')
            country_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.COUNTRY_FIND_BY_UUID_ERROR_DB.phrase
            error_code = VPNCError.COUNTRY_FIND_BY_UUID_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.COUNTRY_FIND_BY_UUID_ERROR_DB.description, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(country_list_db) == 1:
            country_db = country_list_db[0]
        elif len(country_list_db) == 0:
            error_message = VPNCError.COUNTRY_FIND_BY_UUID_ERROR.phrase
            error_code = VPNCError.COUNTRY_FIND_BY_UUID_ERROR.value
            developer_message = VPNCError.COUNTRY_FIND_BY_UUID_ERROR.description
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = VPNCError.COUNTRY_FIND_BY_UUID_ERROR.phrase
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % VPNCError.COUNTRY_FIND_BY_UUID_ERROR.description
            error_code = VPNCError.COUNTRY_FIND_BY_UUID_ERROR.value
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_countrydb_to_country(country_db)

    def __map_countrydb_to_country(self, country_db):
        return Country(
            code=country_db[self._code_field],
            name=country_db[self._name_field],
            created_date=country_db[self._created_date_field],
        )
