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


class VPNSServersConnectionsAPI(ResourceAPI):
    __version__ = 1

    logger = logging.getLogger(__name__)

    __endpoint_name__ = __qualname__
    __api_url__ = 'vpns/servers/<string:server_uuid>/connections'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, VPNSServersConnectionsAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url.replace('/<string:server_uuid>/', '/'), resource_name='', methods=['GET']),
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST', 'DELETE']),
            APIResourceURL(base_url=url, resource_name='<string:conn_uuid>', methods=['GET', 'PUT', 'DELETE'])
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, *args) -> None:
        super().__init__(*args)
        self.__db_storage_service = db_storage_service

    def post(self, server_uuid: str) -> Response:
        super(VPNSServersConnectionsAPI, self).post(req=request)

        request_json = request.json

        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=VPNCError.REQUEST_NO_JSON)

        vpnserver_uuid = request_json.get(VPNServerConnectionDB._server_uuid_field, None)

        self.logger.debug(f"{self.__class__}: check uuids")
        self.logger.debug(f"{self.__class__}: server uuid: {server_uuid}")
        self.logger.debug(f"{self.__class__}: vpnserver_uuid: {vpnserver_uuid}")
        self.logger.debug(f"{self.__class__}: server_uuid != vpnserver_uuid: {server_uuid != vpnserver_uuid}")

        is_valid_server_uuid = check_uuid(server_uuid)
        is_valid_server_uuid_again = check_uuid(vpnserver_uuid)
        if not is_valid_server_uuid or not is_valid_server_uuid_again or server_uuid != vpnserver_uuid:
            return make_error_request_response(http_code=HTTPStatus.BAD_REQUEST,
                                               err=VPNCError.VPNSERVERCONN_IDENTIFIER_ERROR)

        self.logger.debug(f"{self.__class__}: get fields from request_json")

        user_uuid = request_json.get(VPNServerConnectionDB._user_uuid_field, None)
        user_device_uuid = request_json.get(VPNServerConnectionDB._user_device_uuid_field, None)
        ip_device = request_json.get(VPNServerConnectionDB._device_ip_field, None)
        virtual_ip = request_json.get(VPNServerConnectionDB._virtual_ip_field, None)
        bytes_i = request_json.get(VPNServerConnectionDB._bytes_i_field, None)
        bytes_o = request_json.get(VPNServerConnectionDB._bytes_o_field, None)
        connected_since = request_json.get(VPNServerConnectionDB._connected_since_field, None)
        is_connected = request_json.get(VPNServerConnectionDB._is_connected_field, None)

        self.logger.debug(f"{self.__class__}: check req_fields")

        req_fields = {
            'server_uuid': server_uuid,
            'user_uuid': user_uuid,
            'virtual_ip': virtual_ip,
        }

        error_fields = check_required_api_fields(fields=req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        vpnserverconn_db = VPNServerConnectionDB(storage_service=self.__db_storage_service, is_connected=is_connected,
                                                 user_device_uuid=user_device_uuid, server_uuid=server_uuid,
                                                 user_uuid=user_uuid, ip_device=ip_device, virtual_ip=virtual_ip,
                                                 bytes_i=bytes_i, bytes_o=bytes_o, connected_since=connected_since)
        try:
            suuid = vpnserverconn_db.create()
        except VPNException as e:
            self.logger.error(e)
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

    def put(self, server_uuid: str, conn_uuid: str) -> Response:
        request_json = request.json

        is_valid_suuid = check_uuid(conn_uuid)
        is_valid_server_uuid = check_uuid(server_uuid)
        if not is_valid_suuid or not is_valid_server_uuid:
            return make_error_request_response(http_code=HTTPStatus.BAD_REQUEST,
                                               err=VPNCError.VPNSERVERCONN_IDENTIFIER_ERROR)

        user_uuid = request_json.get(VPNServerConnectionDB._user_uuid_field, None)
        user_device_uuid = request_json.get(VPNServerConnectionDB._user_device_uuid_field, None)
        device_ip = request_json.get(VPNServerConnectionDB._device_ip_field, None)
        virtual_ip = request_json.get(VPNServerConnectionDB._virtual_ip_field, None)
        bytes_i = request_json.get(VPNServerConnectionDB._bytes_i_field, None)
        bytes_o = request_json.get(VPNServerConnectionDB._bytes_o_field, None)
        connected_since = request_json.get(VPNServerConnectionDB._connected_since_field, None)
        is_connected = request_json.get(VPNServerConnectionDB._is_connected_field, None)

        vpnserverconn_db = VPNServerConnectionDB(storage_service=self.__db_storage_service, suuid=conn_uuid,
                                                 user_device_uuid=user_device_uuid, server_uuid=server_uuid,
                                                 user_uuid=user_uuid, ip_device=device_ip, virtual_ip=virtual_ip,
                                                 is_connected=is_connected, bytes_i=bytes_i, bytes_o=bytes_o,
                                                 connected_since=connected_since)

        try:
            if user_uuid is not None and user_device_uuid is not None and device_ip is not None and virtual_ip is not None and connected_since is not None and bytes_i is not None and bytes_o is not None \
                    and is_connected is not None:
                self.logger.debug("all required fields filled")
                vpnserverconn_db.update()
            elif bytes_i is not None and bytes_o is not None and is_connected is not None:
                # TODO traffic and active in one sql
                self.logger.debug("update traffic")
                vpnserverconn_db.update_traffic()
                vpnserverconn_db.update_active()
            elif bytes_i is not None and bytes_o is not None:
                self.logger.debug("update traffic")
                vpnserverconn_db.update_traffic()
            elif is_connected is not None:
                self.logger.debug("update is_connected")
                vpnserverconn_db.update_active()
            else:
                self.logger.debug("something bad data links")
                self.logger.debug("user_uuid: " + str(user_uuid))
                self.logger.debug("user_device_uuid: " + str(user_device_uuid))
                self.logger.debug("device_ip: " + str(device_ip))
                self.logger.debug("virtual_ip: " + str(virtual_ip))
                self.logger.debug("bytes_i: " + str(bytes_i))
                self.logger.debug("bytes_o: " + str(bytes_o))
                self.logger.debug("connected_since: " + str(connected_since))
                self.logger.debug("is_connected: " + str(is_connected))
        except VPNException as e:
            self.logger.error(e)
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

    def get(self, server_uuid: str = None, conn_uuid: str = None) -> Response:
        super(VPNSServersConnectionsAPI, self).get(req=request)

        user_uuid = request.args.get('user_uuid', None)
        user_device_uuid = request.args.get('user_device_uuid', None)
        virtual_ip = request.args.get('virtual_ip', None)
        is_connected = request.args.get('is_connected', None)

        if server_uuid is not None:
            is_valid = check_uuid(suuid=server_uuid)
            if not is_valid:
                return make_error_request_response(HTTPStatus.BAD_REQUEST,
                                                   err=VPNCError.VPNSERVERCONN_IDENTIFIER_ERROR)

        vpnserverconn_db = VPNServerConnectionDB(storage_service=self.__db_storage_service, suuid=conn_uuid,
                                                 server_uuid=server_uuid, user_uuid=user_uuid, virtual_ip=virtual_ip,
                                                 user_device_uuid=user_device_uuid)

        if user_device_uuid is not None and is_connected is None:
            is_valid = check_uuid(suuid=user_device_uuid)
            if not is_valid:
                return make_error_request_response(http_code=HTTPStatus.BAD_REQUEST,
                                                   err=VPNCError.VPNSERVERCONN_IDENTIFIER_ERROR)

            vpnserverconn_list = vpnserverconn_db.find_by_user_device()
            vpnserverconn_list_dict = [vpnserverconn_list[i].to_api_dict() for i in
                                       range(0, len(vpnserverconn_list))]
            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                        data=vpnserverconn_list_dict)
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
            return resp

        if user_device_uuid is not None and is_connected is not None:
            is_valid = check_uuid(suuid=user_device_uuid)
            if not is_valid:
                return make_error_request_response(http_code=HTTPStatus.BAD_REQUEST,
                                                   err=VPNCError.VPNSERVERCONN_IDENTIFIER_ERROR)

            # we have to find latest connected connection with specified user_device
            try:
                vpnserverconn = vpnserverconn_db.find_by_server_and_user_device()
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=vpnserverconn.to_api_dict())
                resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                return resp
            except VPNNotFoundException as e:
                self.logger.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
            except VPNException as e:
                self.logger.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp

        if virtual_ip is not None and is_connected is not None:
            # we have to find latest connected connection with specified virtual_ip
            try:
                vpnserverconn = vpnserverconn_db.find_by_server_and_virtual_ip()
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=vpnserverconn.to_api_dict())
                resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                return resp
            except VPNNotFoundException as e:
                self.logger.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
            except VPNException as e:
                self.logger.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp

        if user_uuid is not None:
            # user connections
            is_valid = check_uuid(user_uuid)
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
                self.logger.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
            except VPNException as e:
                self.logger.error(e)
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
                self.logger.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
            except VPNException as e:
                self.logger.error(e)
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
                self.logger.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
            except VPNException as e:
                self.logger.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp

    def delete(self, server_uuid: str = None, conn_uuid: str = None) -> Response:
        is_valid_server_uuid = check_uuid(suuid=server_uuid)
        if not is_valid_server_uuid:
            return make_error_request_response(HTTPStatus.NOT_FOUND, err=VPNCError.BAD_IDENTITY_ERROR)

        vpnserverconn_db = VPNServerConnectionDB(storage_service=self.__db_storage_service, suuid=conn_uuid,
                                                 server_uuid=server_uuid)

        try:
            if conn_uuid is not None:
                # delete specific connection
                is_valid_conn_uuid = check_uuid(suuid=conn_uuid)
                if not is_valid_conn_uuid:
                    return make_error_request_response(HTTPStatus.NOT_FOUND, err=VPNCError.BAD_IDENTITY_ERROR)

                vpnserverconn_db.delete_by_uuid()
            else:
                # delete all connections belongs to server
                vpnserverconn_db.delete_by_server()
        except VPNException as e:
            self.logger.error(e)
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
