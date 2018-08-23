import logging
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import *
from app.model.vpn.server.configuration import VPNServerConfigurationDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import check_uuid
from response import make_api_response, make_error_request_response, check_required_api_fields
from api import ResourceAPI
from response import APIResponseStatus, APIResponse
from rest import APIResourceURL


class VPNSServersConfigurationsAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = __qualname__
    __api_url__ = 'vpns/servers/<string:server_uuid>/configurations'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, VPNSServersConfigurationsAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<string:conf_uuid>', methods=['GET', 'PUT'])
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self, server_uuid: str) -> Response:
        request_json = request.json

        user_uuid = request_json.get(VPNServerConfigurationDB._user_uuid_field, None)
        vpn_device_platform_id = request_json.get(VPNServerConfigurationDB._vpn_device_platform_id_field, None)
        vpn_type_id = request_json.get(VPNServerConfigurationDB._vpn_type_id_field, None)
        configuration = request_json.get(VPNServerConfigurationDB._configuration_field, None)

        req_fields = {
            'user_uuid': user_uuid,
            'vpn_device_platform_id': vpn_device_platform_id,
            'vpn_type_id': vpn_type_id,
            'configuration': configuration,
        }

        error_fields = check_required_api_fields(fields=req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        vpnserverconfig_db = VPNServerConfigurationDB(storage_service=self.__db_storage_service, user_uuid=user_uuid,
                                                      server_uuid=server_uuid, vpn_type_id=vpn_type_id,
                                                      vpn_device_platform_id=vpn_device_platform_id,
                                                      configuration=configuration)
        try:
            suuid = vpnserverconfig_db.create()
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
        resp.headers['Location'] = f"{self._config['API_BASE_URI']/{api_url}/{suuid}}"
        return resp

    def put(self, server_uuid: str, suuid: str) -> Response:
        request_json = request.json

        vpnserverconfig_suuid = request_json.get(VPNServerConfigurationDB._suuid_field, None)

        is_valid_suuid = check_uuid(suuid)
        is_valid_vpnserver_uuid = check_uuid(vpnserverconfig_suuid)
        if not is_valid_suuid or not is_valid_vpnserver_uuid or suuid != vpnserverconfig_suuid:
            return make_error_request_response(http_code=HTTPStatus.BAD_REQUEST,
                                               err=VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR)

        user_uuid = request_json.get(VPNServerConfigurationDB._user_uuid_field, None)
        vpn_type_id = request_json.get(VPNServerConfigurationDB._vpn_type_id_field, None)
        vpn_device_platform_id = request_json.get(VPNServerConfigurationDB._vpn_device_platform_id_field, None)
        configuration = request_json.get(VPNServerConfigurationDB._configuration_field, None)

        req_fields = {
            'user_uuid': user_uuid,
            'vpn_type_id': vpn_type_id,
            'vpn_device_platform_id': vpn_device_platform_id,
            'configuration': configuration,
        }

        error_fields = check_required_api_fields(fields=req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        vpnserverconfig_db = VPNServerConfigurationDB(storage_service=self.__db_storage_service, suuid=suuid,
                                                      user_uuid=user_uuid, server_uuid=server_uuid,
                                                      vpn_device_platform_id=vpn_device_platform_id,
                                                      configuration=configuration)
        try:
            vpnserverconfig_db.update()
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

    def get(self, server_uuid: str, conf_uuid: str = None) -> Response:
        super(VPNSServersConfigurationsAPI, self).get(req=request)

        user_uuid = request.args.get('user_uuid', None)
        platform_id = request.args.get('platform_id', None)
        vpn_type_id = request.args.get('vpn_type_id', None)

        is_valid_server_uuid = check_uuid(suuid=server_uuid)
        if not is_valid_server_uuid:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR)

        req_fields = {
            'user_uuid': user_uuid,
            'platform_id': platform_id,
            'vpn_type_id': vpn_type_id,
        }

        error_fields = check_required_api_fields(fields=req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        vpnserverconfig_db = VPNServerConfigurationDB(storage_service=self.__db_storage_service, suuid=conf_uuid,
                                                      vpn_device_platform_id=platform_id, vpn_type_id=vpn_type_id,
                                                      server_uuid=server_uuid, user_uuid=user_uuid)
        if user_uuid is not None and platform_id is not None and vpn_type_id is not None:
            is_valid_user_uuid = check_uuid(suuid=user_uuid)
            if not is_valid_user_uuid:
                return make_error_request_response(HTTPStatus.BAD_REQUEST,
                                                   err=VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR)

            # user specific configuration
            is_valid = check_uuid(suuid=user_uuid)
            if not is_valid:
                return make_error_request_response(HTTPStatus.BAD_REQUEST,
                                                   err=VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR)
            try:
                vpnserverconfig = vpnserverconfig_db.find_by_user_platform_type()
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=vpnserverconfig.to_api_dict())
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
        elif conf_uuid is not None:
            is_valid = check_uuid(suuid=conf_uuid)
            if not is_valid:
                return make_error_request_response(HTTPStatus.BAD_REQUEST,
                                                   err=VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR)

            # specific configuration
            try:
                vpnserverconfig = vpnserverconfig_db.find_by_suuid()
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=vpnserverconfig.to_api_dict())
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
            # all server configurations
            try:
                vpnserverconfig_list = vpnserverconfig_db.find()
                vpnserverconfig_list_dict = [vpnserverconfig_list[i].to_api_dict() for i in
                                             range(0, len(vpnserverconfig_list))]
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=vpnserverconfig_list_dict)
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
