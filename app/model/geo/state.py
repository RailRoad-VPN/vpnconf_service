import datetime
import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import VPNException, VPNCError, VPNNotFoundException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService


class State(object):
    __version__ = 1

    _code = None
    _state_code = None
    _name = None
    _created_date = None

    def __init__(self, code: str = None, state_code: str = None, name: str = None, created_date: datetime = None):
        self._code = code
        self._state_code = state_code
        self._name = name
        self._created_date = created_date

    def to_dict(self):
        return {
            'code': self._code,
            'state_code': self._state_code,
            'name': self._name,
            'created_date': self._created_date,
        }


class StateStored(State):
    __version__ = 1

    _storage_service = None

    def __init__(self, storage_service: StorageService, **kwargs) -> None:
        super().__init__(**kwargs)

        self._storage_service = storage_service


class StateDB(StateStored):
    __version__ = 1

    _code_field = 'code'
    _state_code_field = 'state_code'
    _name_field = 'name'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('StateDB find method')
        select_sql = 'SELECT * FROM public.state'
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
        select_sql = 'SELECT * FROM public.state WHERE code = ?'
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
                        (code, name) 
                      VALUES 
                        (?, ?)
                     '''
        insert_params = (
            self._code,
            self._name,
        )
        logging.debug('Create StateDB SQL : %s' % insert_sql)

        try:
            logging.debug('Call database service')
            data = self._storage_service.create(sql=insert_sql, data=insert_params, is_return=True)
            self._code = data[self._code_field]
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
                        name = ?
                    WHERE 
                        code = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._name,
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
            name=state_db[self._name_field],
            created_date=state_db[self._created_date_field],
        )

    @property
    def code_field(self):
        return type(self)._code_field

    @property
    def state_code_field(self):
        return type(self)._state_code_field

    @property
    def name_field(self):
        return type(self)._name_field

    @property
    def created_date_field(self):
        return type(self)._created_date_field
