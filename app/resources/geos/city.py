import logging
import sys
import uuid
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import *
from app.model.geo.city import CityDB
from rest import APIResourceURL

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import make_api_response, make_error_request_response
from api import ResourceAPI
from response import APIResponseStatus, APIResponse


class CityAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = 'CityAPI'
    __api_url__ = 'geo_positions/cities'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, CityAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<int:sid>', methods=['GET', 'PUT']),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        name = request_json.get(CityDB._name_field, None)

        city_db = CityDB(storage_service=self.__db_storage_service, name=name)

        try:
            sid = city_db.create()
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        resp = make_api_response(http_code=HTTPStatus.CREATED)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], self.__api_url__, sid)
        return resp

    def put(self, sid: int) -> Response:
        request_json = request.json
        city_sid = request_json.get(CityDB._sid_field, None)

        try:
            sid = int(sid)
            city_sid = int(city_sid)
        except ValueError:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=VPNCError.CITY_IDENTIFIER_ERROR)

        if sid != city_sid:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=VPNCError.CITY_IDENTIFIER_ERROR)

        name = request_json.get(CityDB._name_field, None)

        city_db = CityDB(storage_service=self.__db_storage_service, sid=sid, name=name)

        try:
            city_db.update()
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        resp = make_api_response(http_code=HTTPStatus.OK)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], self.__api_url__, uuid)
        return resp

    def get(self, sid: int = None) -> Response:
        super(CityAPI, self).get(req=request)
        if sid is not None:
            try:
                sid = int(sid)
            except ValueError:
                return make_error_request_response(HTTPStatus.BAD_REQUEST, err=VPNCError.CITY_IDENTIFIER_ERROR)

            city_db = CityDB(storage_service=self.__db_storage_service, sid=sid)

            try:
                city = city_db.find_by_sid()
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)

            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                        data=city.to_api_dict())
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
        else:
            city_db = CityDB(storage_service=self.__db_storage_service, limit=self.pagination.limit,
                             offset=self.pagination.offset)
            try:
                city_list = city_db.find()
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)

            cities_dict = [city_list[i].to_api_dict() for i in range(0, len(city_list))]
            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK, data=cities_dict,
                                        limit=self.pagination.limit, offset=self.pagination.offset)
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)

        return resp
