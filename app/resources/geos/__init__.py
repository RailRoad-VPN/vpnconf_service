import json
import logging
import sys
import uuid
from http import HTTPStatus

from flask import Response, request, make_response

from app.exception import *
from app.model.geo import GeoDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import JSONDecimalEncoder, make_api_response
from api import ResourceAPI
from response import APIResponseStatus, APIResponse


class GeoAPI(ResourceAPI):
    __version__ = 1

    __api_url__ = 'geo_positions'

    _config = None

    __db_storage_service = None

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        latitude = request_json.get(GeoDB._latitude_field, None)
        longitude = request_json.get(GeoDB._longitude_field, None)
        country_code = request_json.get(GeoDB._country_code_field, None)
        state_code = request_json.get(GeoDB._state_code_field, None)
        region_common = request_json.get(GeoDB._region_common_field, None)
        region_dvd = request_json.get(GeoDB._region_dvd_field, None)
        region_xbox360 = request_json.get(GeoDB._region_xbox360_field, None)
        region_xboxone = request_json.get(GeoDB._region_xboxone_field, None)
        region_playstation3 = request_json.get(GeoDB._region_playstation3_field, None)
        region_playstation4 = request_json.get(GeoDB._region_playstation4_field, None)
        region_nintendo = request_json.get(GeoDB._region_nintendo_field, None)

        geo_db = GeoDB(storage_service=self.__db_storage_service, latitude=latitude, longitude=latitude,
                       country_code=longitude, state_code=country_code, city_id=state_code, region_common=region_common,
                       region_dvd=region_dvd, region_xbox360=region_xbox360, region_xboxone=region_xboxone,
                       region_playstation3=region_playstation3, region_playstation4=region_playstation4,
                       region_nintendo=region_nintendo)

        try:
            sid = geo_db.create()
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(json.dumps(response_data.serialize()), http_code)

        resp = make_api_response('', HTTPStatus.CREATED)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], self.__api_url__, sid)
        return resp

    def put(self, sid: int) -> Response:
        request_json = request.json
        geo_id = request_json.get(GeoDB._sid_field, None)

        try:
            sid = int(sid)
            geo_id = int(geo_id)
        except ValueError:
            error = VPNCError.GEO_IDENTIFIER_ERROR.phrase
            error_code = VPNCError.GEO_IDENTIFIER_ERROR
            developer_message = VPNCError.GEO_IDENTIFIER_ERROR.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(json.dumps(response_data.serialize()), http_code)
            return resp

        if sid != geo_id:
            error = VPNCError.GEO_IDENTIFIER_ERROR.phrase
            error_code = VPNCError.GEO_IDENTIFIER_ERROR
            developer_message = VPNCError.GEO_IDENTIFIER_ERROR.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(json.dumps(response_data.serialize()), http_code)
            return resp

        latitude = request_json.get(GeoDB._latitude_field, None)
        longitude = request_json.get(GeoDB._longitude_field, None)
        country_code = request_json.get(GeoDB._country_code_field, None)
        state_code = request_json.get(GeoDB._state_code_field, None)
        region_common = request_json.get(GeoDB._region_common_field, None)
        region_dvd = request_json.get(GeoDB._region_dvd_field, None)
        region_xbox360 = request_json.get(GeoDB._region_xbox360_field, None)
        region_xboxone = request_json.get(GeoDB._region_xboxone_field, None)
        region_playstation3 = request_json.get(GeoDB._region_playstation3_field, None)
        region_playstation4 = request_json.get(GeoDB._region_playstation4_field, None)
        region_nintendo = request_json.get(GeoDB._region_nintendo_field, None)

        geo_db = GeoDB(storage_service=self.__db_storage_service, sid=sid, latitude=latitude, longitude=latitude,
                       country_code=longitude, state_code=country_code, city_id=state_code, region_common=region_common,
                       region_dvd=region_dvd, region_xbox360=region_xbox360, region_xboxone=region_xboxone,
                       region_playstation3=region_playstation3, region_playstation4=region_playstation4,
                       region_nintendo=region_nintendo)

        try:
            geo_db.update()
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(json.dumps(response_data.serialize()), http_code)

        resp = make_api_response('', HTTPStatus.OK)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], self.__api_url__, uuid)
        return resp

    def get(self, sid: int = None) -> Response:
        if sid is not None:
            try:
                sid = int(sid)
            except ValueError:
                error = VPNCError.GEO_IDENTIFIER_ERROR.phrase
                error_code = VPNCError.GEO_IDENTIFIER_ERROR
                developer_message = VPNCError.GEO_IDENTIFIER_ERROR.description
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(json.dumps(response_data.serialize()), http_code)
                return resp

            geo_db = GeoDB(storage_service=self.__db_storage_service, sid=sid)

            try:
                geo = geo_db.find_by_sid()
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(json.dumps(response_data.serialize()), http_code)
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(json.dumps(response_data.serialize()), http_code)

            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                        data=geo.to_api_dict())
            resp = make_api_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)
        else:
            geo_db = GeoDB(storage_service=self.__db_storage_service)

            try:
                geo_list = geo_db.find()
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(json.dumps(response_data.serialize()), http_code)
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(json.dumps(response_data.serialize()), http_code)

            geos_dict = [geo_list[i].to_api_dict() for i in range(0, len(geo_list))]
            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK, data=geos_dict)
            resp = make_api_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)

        return resp
