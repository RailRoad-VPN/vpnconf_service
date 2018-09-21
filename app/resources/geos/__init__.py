import logging
import uuid
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import *
from app.model.geo import GeoDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from response import make_api_response, make_error_request_response, check_required_api_fields
from api import ResourceAPI
from response import APIResponseStatus, APIResponse
from rest import APIResourceURL


class GeosAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = __qualname__
    __api_url__ = 'geo_positions'

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, GeosAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<int:sid>', methods=['GET', 'PUT']),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, *args) -> None:
        super().__init__(*args)
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=VPNCError.REQUEST_NO_JSON)

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

        req_fields = {
            'latitude': latitude,
            'longitude': longitude,
            'country_code': country_code,
            'state_code': state_code,
            'region_common': region_common,
            'region_dvd': region_dvd,
            'region_xbox360': region_xbox360,
            'region_xboxone': region_xboxone,
            'region_playstation3': region_playstation3,
            'region_playstation4': region_playstation4,
            'region_nintendo': region_nintendo,
        }

        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

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
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.CREATED)
        resp = make_api_response(data=response_data, http_code=HTTPStatus.CREATED)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], self.__api_url__, sid)
        return resp

    def put(self, sid: int) -> Response:
        request_json = request.json
        geo_id = request_json.get(GeoDB._sid_field, None)

        try:
            sid = int(sid)
            geo_id = int(geo_id)
        except ValueError:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=VPNCError.GEO_IDENTIFIER_ERROR)

        if sid != geo_id:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=VPNCError.GEO_IDENTIFIER_ERROR)

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

        req_fields = {
            'latitude': latitude,
            'longitude': longitude,
            'country_code': country_code,
            'state_code': state_code,
            'region_common': region_common,
            'region_dvd': region_dvd,
            'region_xbox360': region_xbox360,
            'region_xboxone': region_xboxone,
            'region_playstation3': region_playstation3,
            'region_playstation4': region_playstation4,
            'region_nintendo': region_nintendo,
        }

        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

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
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        resp = make_api_response(http_code=HTTPStatus.OK)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], self.__api_url__, uuid)
        return resp

    def get(self, sid: int = None) -> Response:
        super(GeosAPI, self).get(req=request)
        if sid is not None:
            try:
                sid = int(sid)
            except ValueError:
                return make_error_request_response(HTTPStatus.BAD_REQUEST, err=VPNCError.GEO_IDENTIFIER_ERROR)

            geo_db = GeoDB(storage_service=self.__db_storage_service, sid=sid)

            try:
                geo = geo_db.find_by_sid()
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
                                        data=geo.to_api_dict())
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
        else:
            geo_db = GeoDB(storage_service=self.__db_storage_service, limit=self.pagination.limit,
                           offset=self.pagination.offset)

            try:
                geo_list = geo_db.find()
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

            geos_dict = [geo_list[i].to_api_dict() for i in range(0, len(geo_list))]
            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK, data=geos_dict,
                                        limit=self.pagination.limit, offset=self.pagination.offset)
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)

        return resp
