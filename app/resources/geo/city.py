import json
import logging
import sys
import uuid
from http import HTTPStatus

from flask import Response, request, make_response

from app.exception import *
from app.model.geo.city import CityDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import JSONDecimalEncoder
from api import ResourceAPI
from response import APIResponseStatus, APIResponse


class CityAPI(ResourceAPI):
    __version__ = 1

    __api_url__ = 'geo/cities'

    _config = None

    __db_storage_service = None

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        name = request_json.get(CityDB.name_field, None)

        city_db = CityDB(storage_service=self.__db_storage_service, name=name)

        try:
            sid = city_db.create()
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            if error_code == VPNCError.CITY_CREATE_ERROR:
                http_code = HTTPStatus.BAD_REQUEST
            else:
                http_code = HTTPStatus.INTERNAL_SERVER_ERROR
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_response(json.dumps(response_data.serialize()), http_code)

        resp = make_response('', HTTPStatus.CREATED)
        resp.headers['Location'] = '%s/%s/sid/%s' % (self._config['API_BASE_URI'], self.__api_url__, sid)
        return resp

    def put(self, sid: str = None) -> Response:
        request_json = request.json
        city_id = request_json.get(CityDB.sid_field, None)
        if sid != city_id:
            error = VPNCError.CITY_FINDBYID_ERROR.phrase
            error_code = VPNCError.CITY_FINDBYID_ERROR
            developer_message = VPNCError.CITY_FINDBYID_ERROR.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_response(json.dumps(response_data.serialize()), http_code)
            return resp

        name = request_json.get(CityDB.name_field, None)

        city_db = CityDB(storage_service=self.__db_storage_service, name=name)

        try:
            city_db.update()
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            if error_code == VPNCError.CITY_UPDATE_ERROR:
                http_code = HTTPStatus.BAD_REQUEST
            else:
                http_code = HTTPStatus.INTERNAL_SERVER_ERROR
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_response(json.dumps(response_data.serialize()), http_code)

        resp = make_response('', HTTPStatus.OK)
        resp.headers['Location'] = '%s/%s/sid/%s' % (self._config['API_BASE_URI'], self.__api_url__, uuid)
        return resp

    def get(self, sid: str = None) -> Response:
        if sid is not None:
            try:
                sid = int(sid)
            except ValueError:
                error = VPNCError.CITY_FINDBYID_ERROR.phrase
                error_code = VPNCError.CITY_FINDBYID_ERROR
                developer_message = VPNCError.CITY_FINDBYID_ERROR.description
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_response(json.dumps(response_data.serialize()), http_code)
                return resp

            city_db = CityDB(storage_service=self.__db_storage_service, sid=sid)

            city = city_db.find_by_sid()
            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                        data=city.to_dict())
            resp = make_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)
        else:
            city_db = CityDB(storage_service=self.__db_storage_service)

            city_list = city_db.find()
            cities_dict = {city_list[i]: city_list[i + 1] for i in range(0, len(city_list), 2)}
            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                        data=cities_dict)
            resp = make_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)

        return resp
