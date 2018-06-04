import json
import logging
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import *
from app.model.vpn.server import VPNServerDB
from rest import APIResourceURL

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import JSONDecimalEncoder, check_uuid, make_api_response
from api import ResourceAPI
from response import APIResponseStatus, APIResponse


class VPNServerAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = 'VPNServersAPI'
    __api_url__ = 'vpns/servers'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, VPNServerAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<string:suuid>', methods=['GET', 'PUT']),
            APIResourceURL(base_url=url, resource_name='type/<int:type_id>', methods=['GET']),
            APIResourceURL(base_url=url, resource_name='status/<int:status_id>', methods=['GET']),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        if request_json is None:
            error = VPNCError.REQUEST_NO_JSON.phrase
            error_code = VPNCError.REQUEST_NO_JSON
            developer_message = VPNCError.REQUEST_NO_JSON.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(response_data, http_code)

        version = request_json.get(VPNServerDB._version_field, None)
        condition_version = request_json.get(VPNServerDB._condition_version_field, None)
        type_id = request_json.get(VPNServerDB._type_id_field, None)
        status_id = request_json.get(VPNServerDB._status_id_field, None)
        bandwidth = request_json.get(VPNServerDB._bandwidth_field, None)
        load = request_json.get(VPNServerDB._load_field, None)
        geo_position_id = request_json.get(VPNServerDB._geo_position_id_field, None)

        vpnserver_db = VPNServerDB(storage_service=self.__db_storage_service, version=version,
                                   condition_version=condition_version, type_id=type_id, status_id=status_id,
                                   bandwidth=bandwidth, load=load, geo_position_id=geo_position_id)

        try:
            suuid = vpnserver_db.create()
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(response_data, http_code)

        response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.CREATED)
        resp = make_api_response(response_data, HTTPStatus.CREATED)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], self.__api_url__, suuid)
        return resp

    def put(self, suuid: str) -> Response:
        request_json = request.json

        if request_json is None:
            error = VPNCError.REQUEST_NO_JSON.phrase
            error_code = VPNCError.REQUEST_NO_JSON
            developer_message = VPNCError.REQUEST_NO_JSON.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(response_data, http_code)

        vpnserver_suuid = request_json.get(VPNServerDB._suuid_field, None)

        is_valid_suuid = check_uuid(suuid)
        is_valid_vpnserver_suuid = check_uuid(vpnserver_suuid)
        if not is_valid_suuid or not is_valid_vpnserver_suuid:
            error = VPNCError.VPNSERVER_IDENTIFIER_ERROR.phrase
            error_code = VPNCError.VPNSERVER_IDENTIFIER_ERROR
            developer_message = VPNCError.VPNSERVER_IDENTIFIER_ERROR.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(response_data, http_code)
            return resp

        if suuid != vpnserver_suuid:
            error = VPNCError.VPNSERVER_IDENTIFIER_ERROR.phrase
            error_code = VPNCError.VPNSERVER_IDENTIFIER_ERROR
            developer_message = VPNCError.VPNSERVER_IDENTIFIER_ERROR.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(response_data, http_code)
            return resp

        version = request_json.get(VPNServerDB._version_field, None)
        condition_version = request_json.get(VPNServerDB._condition_version_field, None)
        type_id = request_json.get(VPNServerDB._type_id_field, None)
        status_id = request_json.get(VPNServerDB._status_id_field, None)
        bandwidth = request_json.get(VPNServerDB._bandwidth_field, None)
        load = request_json.get(VPNServerDB._load_field, None)
        geo_position_id = request_json.get(VPNServerDB._geo_position_id_field, None)

        vpnserver_db = VPNServerDB(storage_service=self.__db_storage_service, suuid=suuid, version=version,
                                   condition_version=condition_version, type_id=type_id, status_id=status_id,
                                   bandwidth=bandwidth, load=load, geo_position_id=geo_position_id)

        try:
            vpnserver_db.update()
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(response_data, http_code)

        response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.NO_CONTENT)
        resp = make_api_response(response_data, HTTPStatus.NO_CONTENT)
        return resp

    def get(self, suuid: str = None, type_id: int = None, status_id: int = None) -> Response:
        super(VPNServerAPI, self).get(req=request)

        vpnserver_db = VPNServerDB(storage_service=self.__db_storage_service, suuid=suuid, type_id=type_id,
                                   status_id=status_id,
                                   limit=self.pagination.limit, offset=self.pagination.offset)
        if suuid is not None:
            is_valid = check_uuid(suuid)
            if not is_valid:
                error = VPNCError.VPNSERVER_IDENTIFIER_ERROR.phrase
                error_code = VPNCError.VPNSERVER_IDENTIFIER_ERROR
                developer_message = VPNCError.VPNSERVER_IDENTIFIER_ERROR.description
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(response_data, http_code)
                return resp

            try:
                vpnserver = vpnserver_db.find_by_suuid()
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(response_data, http_code)
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(response_data, http_code)

            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                        data=vpnserver.to_api_dict())
            resp = make_api_response(response_data, HTTPStatus.OK)
        elif type_id is not None:
            # list of servers by specific type id
            try:
                vpnserver_list = vpnserver_db.find_by_type_id()
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(response_data, http_code)
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(response_data, http_code)

            vpnservers_dict = [vpnserver_list[i].to_api_dict() for i in range(0, len(vpnserver_list))]
            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                        data=vpnservers_dict, limit=self.pagination.limit,
                                        offset=self.pagination.offset)
            resp = make_api_response(response_data, HTTPStatus.OK)
        elif status_id is not None:
            # list of servers by specific status id
            try:
                vpnserver_list = vpnserver_db.find_by_status_id()
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(response_data, http_code)
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(response_data, http_code)

            vpnservers_dict = [vpnserver_list[i].to_api_dict() for i in range(0, len(vpnserver_list))]
            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                        data=vpnservers_dict, limit=self.pagination.limit,
                                        offset=self.pagination.offset)
            resp = make_api_response(response_data, HTTPStatus.OK)
        else:
            # list of all servers
            try:
                vpnserver_list = vpnserver_db.find()
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(response_data, http_code)
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(response_data, http_code)

            vpnservers_dict = [vpnserver_list[i].to_api_dict() for i in range(0, len(vpnserver_list))]
            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                        data=vpnservers_dict, limit=self.pagination.limit,
                                        offset=self.pagination.offset)
            resp = make_api_response(response_data, HTTPStatus.OK)

        return resp
