import datetime
import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import VPNException, VPNCError, VPNNotFoundException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class State(object):
    __version__ = 1

    _code = None
    _country_code = None
    _name = None
    _created_date = None

    def __init__(self, code: str = None, country_code: int = None, name: str = None, created_date: datetime = None):
        self._code = code
        self._country_code = country_code
        self._name = name
        self._created_date = created_date

    def to_dict(self):
        return {
            'code': self._code,
            'country_code': self._country_code,
            'name': self._name,
            'created_date': self._created_date,
        }

    def to_api_dict(self):
        return {
            'code': self._code,
            'country_code': self._country_code,
            'name': self._name,
        }


class StateStored(StoredObject, State):
    __version__ = 1

    def __init__(self, storage_service: StorageService, code: str = None, country_code: int = None, name: str = None,
                 created_date: datetime = None, limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        State.__init__(self, code=code, country_code=country_code, name=name, created_date=created_date)


class StateDB(StateStored):
    __version__ = 1

    _code_field = 'code'
    _country_code_field = 'country_code'
    _name_field = 'name'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('StateDB find method')
        select_sql = '''
                      SELECT 
                        code
                        country_code,
                        name,
                        to_json(created_date) AS created_date 
                      FROM public.state
                      '''
        if self._limit:
            select_sql += "\nLIMIT %s\nOFFSET %s" % (self._limit, self._offset)
        logging.debug('Select SQL: %s' % select_sql)

        try:
            logging.debug('Call database service')
            state_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = VPNCError.STATE_FIND_ERROR_DB.phrase
            error_code = VPNCError.STATE_FIND_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.STATE_FIND_ERROR_DB.description, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        state_list = []

        for state_db in state_list_db:
            state = self.__map_statedb_to_state(state_db)
            state_list.append(state)

        if len(state_list) == 0:
            logging.warning('Empty State list of method find_all. Very strange behaviour.')

        return state_list

    def find_by_code(self):
        logging.info('StateDB find_by_code method')
        select_sql = '''
                      SELECT 
                        code
                        country_code,
                        name,
                        to_json(created_date) AS created_date 
                      FROM public.state 
                      WHERE code = ?
                      '''
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._code,)

        try:
            logging.debug('Call database service')
            state_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.STATE_FIND_BY_UUID_ERROR_DB.phrase
            error_code = VPNCError.STATE_FIND_BY_UUID_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.STATE_FIND_BY_UUID_ERROR_DB.description, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(state_list_db) == 1:
            state_db = state_list_db[0]
        elif len(state_list_db) == 0:
            error_message = VPNCError.STATE_FIND_BY_UUID_ERROR.phrase
            error_code = VPNCError.STATE_FIND_BY_UUID_ERROR.value
            developer_message = VPNCError.STATE_FIND_BY_UUID_ERROR.description
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = VPNCError.STATE_FIND_BY_UUID_ERROR.phrase
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % VPNCError.STATE_FIND_BY_UUID_ERROR.description
            error_code = VPNCError.STATE_FIND_BY_UUID_ERROR.value
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_statedb_to_state(state_db)

    def create(self):
        logging.info('StateDB create method')
        insert_sql = '''
                      INSERT INTO public.state 
                        (code, country_code, name) 
                      VALUES 
                        (?, ?, ?)
                     '''
        insert_params = (
            self._code,
            self._country_code,
            self._name,
        )
        logging.debug('Create StateDB SQL : %s' % insert_sql)

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
            error_message = VPNCError.STATE_CREATE_ERROR_DB.phrase
            error_code = VPNCError.STATE_CREATE_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.STATE_CREATE_ERROR_DB.description, e.pgcode, e.pgerror)

            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('StateDB created.')

        return self._code

    def update(self):
        logging.info('State update method')

        update_sql = '''
                    UPDATE public.state 
                    SET
                        name = ?,
                        country_code = ?
                    WHERE 
                        code = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._name,
            self._country_code,
            self._code,
        )

        try:
            logging.debug("Call database service")
            self._storage_service.update(sql=update_sql, data=update_params)
            logging.debug('State updated.')
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.STATE_UPDATE_ERROR_DB.phrase
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    VPNCError.STATE_UPDATE_ERROR_DB.description, e.pgcode, e.pgerror)
            error_code = VPNCError.STATE_UPDATE_ERROR_DB.value
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

    def __map_statedb_to_state(self, state_db):
        return State(
            code=state_db[self._code_field],
            country_code=state_db[self._country_code_field],
            name=state_db[self._name_field],
            created_date=state_db[self._created_date_field],
        )
