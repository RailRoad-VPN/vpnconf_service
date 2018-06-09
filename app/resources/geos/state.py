import logging
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import *
from app.model.geo.state import StateDB
from rest import APIResourceURL

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import make_api_response
from api import ResourceAPI
from response import APIResponseStatus, APIResponse


class StateAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = 'StateAPI'
    __api_url__ = 'geo_positions/states'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, StateAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<string:code>', methods=['GET', 'PUT']),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        name = request_json.get(StateDB._name_field, None)

        state_db = StateDB(storage_service=self.__db_storage_service, name=name)

        try:
            code = state_db.create()
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        resp = make_api_response(http_code=HTTPStatus.CREATED)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], self.__api_url__, code)
        return resp

    def put(self, code: str) -> Response:
        request_json = request.json
        state_code = request_json.get(StateDB._code_field, None)

        if code != state_code:
            error = VPNCError.STATE_IDENTIFIER_ERROR.message
            error_code = VPNCError.STATE_IDENTIFIER_ERROR
            developer_message = VPNCError.STATE_IDENTIFIER_ERROR.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(data=response_data, http_code=http_code)
            return resp

        name = request_json.get(StateDB._name_field, None)

        state_db = StateDB(storage_service=self.__db_storage_service, code=code, name=name)

        try:
            state_db.update()
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        resp = make_api_response(http_code=HTTPStatus.OK)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], self.__api_url__, code)
        return resp

    def get(self, code: str = None) -> Response:
        super(StateAPI, self).get(req=request)
        if code is not None:
            state_db = StateDB(storage_service=self.__db_storage_service, code=code)

            try:
                state = state_db.find_by_code()
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)

            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                        data=state.to_api_dict())
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
        else:
            state_db = StateDB(storage_service=self.__db_storage_service, limit=self.pagination.limit,
                               offset=self.pagination.offset)
            try:
                state_list = state_db.find()
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)

            states_dict = [state_list[i].to_api_dict() for i in range(0, len(state_list))]
            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK, data=states_dict,
                                        limit=self.pagination.limit, offset=self.pagination.offset)
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)

        return resp
