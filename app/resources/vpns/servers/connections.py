import logging
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import *
from app.model.vpn.server.connection import VPNServerConnectionDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import check_uuid
from response import make_api_response, make_error_request_response, check_required_api_fields
from api import ResourceAPI
from response import APIResponseStatus, APIResponse
from rest import APIResourceURL


class VPNServerConnectionAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = 'VPNServerConnectionAPI'
    __api_url__ = 'vpns/servers/<string:server_uuid>/connections'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, VPNServerConnectionAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<string:conn_uuid>', methods=['GET', 'PUT'])
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        server_uuid = request_json.get(VPNServerConnectionDB._server_uuid_field, None)
        user_uuid = request_json.get(VPNServerConnectionDB._user_uuid_field, None)
        user_device_uuid = request_json.get(VPNServerConnectionDB._user_device_uuid_field, None)
        ip_device = request_json.get(VPNServerConnectionDB._ip_device_field, None)
        virtual_ip = request_json.get(VPNServerConnectionDB._virtual_ip_field, None)
        bytes_i = request_json.get(VPNServerConnectionDB._bytes_i_field, None)
        bytes_o = request_json.get(VPNServerConnectionDB._bytes_o_field, None)
        last_ref = request_json.get(VPNServerConnectionDB._last_ref_field, None)
        connected_since = request_json.get(VPNServerConnectionDB._connected_since_field, None)

        req_fields = {
            'server_uuid': server_uuid,
            'user_uuid': user_uuid,
            'user_device_uuid': user_device_uuid,
        }

        error_fields = check_required_api_fields(fields=req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        vpnserverconn_db = VPNServerConnectionDB(storage_service=self.__db_storage_service, suuid=suuid,
                                                 server_uuid=server_uuid, user_uuid=user_uuid, ip_device=ip_device,
                                                 virtual_ip=virtual_ip, bytes_i=bytes_i, bytes_o=bytes_o,
                                                 last_ref=last_ref, connected_since=connected_since)
        try:
            suuid = vpnserverconn_db.create()
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

        api_url = self.__api_url__.replace("<string:server_uuid>", server_uuid)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], api_url, suuid)
        return resp

    def put(self, suuid: str) -> Response:
        request_json = request.json

        vpnserverconn_suuid = request_json.get(VPNServerConnectionDB._suuid_field, None)

        is_valid_suuid = check_uuid(suuid)
        is_valid_vpnserver_uuid = check_uuid(vpnserverconn_suuid)
        if not is_valid_suuid or not is_valid_vpnserver_uuid or suuid != vpnserverconn_suuid:
            return make_error_request_response(http_code=HTTPStatus.BAD_REQUEST,
                                               err=VPNCError.VPNSERVERCONN_IDENTIFIER_ERROR)

        suuid = request_json.get(VPNServerConnectionDB._suuid_field, None)
        server_uuid = request_json.get(VPNServerConnectionDB._server_uuid_field, None)
        user_uuid = request_json.get(VPNServerConnectionDB._user_uuid_field, None)
        user_device_uuid = request_json.get(VPNServerConnectionDB._user_device_uuid_field, None)
        ip_device = request_json.get(VPNServerConnectionDB._ip_device_field, None)
        virtual_ip = request_json.get(VPNServerConnectionDB._virtual_ip_field, None)
        bytes_i = request_json.get(VPNServerConnectionDB._bytes_i_field, None)
        bytes_o = request_json.get(VPNServerConnectionDB._bytes_o_field, None)
        last_ref = request_json.get(VPNServerConnectionDB._last_ref_field, None)
        connected_since = request_json.get(VPNServerConnectionDB._connected_since_field, None)

        req_fields = {
            'server_uuid': server_uuid,
            'user_uuid': user_uuid,
            'user_device_uuid': user_device_uuid,
        }

        error_fields = check_required_api_fields(fields=req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        vpnserverconn_db = VPNServerConnectionDB(storage_service=self.__db_storage_service, suuid=suuid,
                                                 server_uuid=server_uuid, user_uuid=user_uuid, ip_device=ip_device,
                                                 virtual_ip=virtual_ip, bytes_i=bytes_i, bytes_o=bytes_o,
                                                 last_ref=last_ref, connected_since=connected_since)

        try:
            vpnserverconn_db.update()
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK)
        resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
        return resp

    def get(self, server_uuid: str, conn_uuid: str = None) -> Response:
        super(VPNServerConnectionAPI, self).get(req=request)

        user_uuid = request.args.get('user_uuid', None)

        is_valid = check_uuid(suuid=server_uuid)
        if not is_valid:
            return make_error_request_response(HTTPStatus.BAD_REQUEST,
                                               err=VPNCError.VPNSERVERCONN_IDENTIFIER_ERROR)

        vpnserverconn_db = VPNServerConnectionDB(storage_service=self.__db_storage_service, suuid=conn_uuid,
                                                 server_uuid=server_uuid, user_uuid=user_uuid)
        if user_uuid is not None:
            # user connection
            is_valid = check_uuid(server_uuid)
            if not is_valid:
                return make_error_request_response(http_code=HTTPStatus.BAD_REQUEST,
                                                   err=VPNCError.VPNSERVERCONN_IDENTIFIER_ERROR)

            try:
                vpnserverconn_list = vpnserverconn_db.find_by_server_and_user()
                vpnserverconn_list_dict = [vpnserverconn_list[i].to_api_dict() for i in
                                           range(0, len(vpnserverconn_list))]
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=vpnserverconn_list_dict)
                resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                return resp
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
        elif conn_uuid is not None:
            is_valid = check_uuid(suuid=conn_uuid)
            if not is_valid:
                return make_error_request_response(HTTPStatus.BAD_REQUEST,
                                                   err=VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR)

            # specific server connection
            try:
                vpnserverconn = vpnserverconn_db.find_by_suuid()
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=vpnserverconn.to_api_dict())
                resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                return resp
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
        else:
            # all server connections
            try:
                vpnserverconn_list = vpnserverconn_db.find_by_server_uuid()
                vpnserverconn_list_dict = [vpnserverconn_list[i].to_api_dict() for i in
                                           range(0, len(vpnserverconn_list))]
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=vpnserverconn_list_dict)
                resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                return resp
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
