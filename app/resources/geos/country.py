import logging
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import *
from app.model.geo.country import CountryDB
from rest import APIResourceURL

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from response import make_api_response, make_error_request_response
from api import ResourceAPI
from response import APIResponseStatus, APIResponse


class CountryAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = 'CountryAPI'
    __api_url__ = 'geo_positions/countries'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, CountryAPI.__api_url__)
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
        return make_error_request_response(HTTPStatus.METHOD_NOT_ALLOWED, err=VPNCError.METHOD_NOT_ALLOWED)

    def put(self, code: str) -> Response:
        return make_error_request_response(HTTPStatus.METHOD_NOT_ALLOWED, err=VPNCError.METHOD_NOT_ALLOWED)

    def get(self, code: int = None) -> Response:
        super(CountryAPI, self).get(req=request)
        if code is not None:
            country_db = CountryDB(storage_service=self.__db_storage_service, code=code)

            try:
                country = country_db.find_by_code()
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
                                        data=country.to_api_dict())
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
        else:
            country_db = CountryDB(storage_service=self.__db_storage_service, limit=self.pagination.limit,
                                   offset=self.pagination.offset)
            try:
                country_list = country_db.find()
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

            countries_dict = [country_list[i].to_api_dict() for i in range(0, len(country_list))]
            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK, data=countries_dict,
                                        limit=self.pagination.limit, offset=self.pagination.offset)
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)

        return resp
