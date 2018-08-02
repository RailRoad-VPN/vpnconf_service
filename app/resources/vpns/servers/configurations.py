import logging
import sys
import uuid
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import *
from app.model.vpn.server.configuration import VPNServerConfigurationDB
from rest import APIResourceURL

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import check_uuid
from response import make_api_response
from api import ResourceAPI
from response import APIResponseStatus, APIResponse


class VPNServerConfigurationAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = 'VPNServerConfigurationAPI'
    __api_url__ = 'vpns/servers/<string:server_uuid>/configurations'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, VPNServerConfigurationAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='user/<string:user_uuid>', methods=['GET', 'PUT'])
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        user_uuid = request_json.get(VPNServerConfigurationDB._user_uuid_field, None)
        server_uuid = request_json.get(VPNServerConfigurationDB._server_uuid_field, None)
        file_path = request_json.get(VPNServerConfigurationDB._file_path_field, None)
        configuration = request_json.get(VPNServerConfigurationDB._configuration_field, None)

        vpnserverconfig_db = VPNServerConfigurationDB(storage_service=self.__db_storage_service, user_uuid=user_uuid,
                                                      server_uuid=server_uuid, file_path=file_path,
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
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], self.__api_url__, suuid)
        return resp

    def put(self, suuid: str) -> Response:
        request_json = request.json

        vpnserverconfig_suuid = request_json.get(VPNServerConfigurationDB._suuid_field, None)

        is_valid_suuid = check_uuid(suuid)
        is_valid_vpnserver_uuid = check_uuid(vpnserverconfig_suuid)
        if not is_valid_suuid or not is_valid_vpnserver_uuid:
            error = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR.message
            error_code = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR
            developer_message = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(data=response_data, http_code=http_code)
            return resp

        if suuid != vpnserverconfig_suuid:
            error = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR.message
            error_code = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR
            developer_message = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(data=response_data, http_code=http_code)
            return resp

        user_uuid = request_json.get(VPNServerConfigurationDB._user_uuid_field, None)
        server_uuid = request_json.get(VPNServerConfigurationDB._server_uuid_field, None)
        file_path = request_json.get(VPNServerConfigurationDB._file_path_field, None)
        configuration = request_json.get(VPNServerConfigurationDB._configuration_field, None)

        vpnserverconfig_db = VPNServerConfigurationDB(storage_service=self.__db_storage_service, suuid=suuid,
                                                      user_uuid=user_uuid, server_uuid=server_uuid,
                                                      file_path=file_path, configuration=configuration)

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

        resp = make_api_response(http_code=HTTPStatus.OK)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], self.__api_url__, uuid)
        return resp

    def get(self, server_uuid: str, user_uuid: str = None) -> Response:
        super(VPNServerConfigurationAPI, self).get(req=request)

        vpnserverconfig_db = VPNServerConfigurationDB(storage_service=self.__db_storage_service,
                                                      server_uuid=server_uuid, user_uuid=user_uuid)
        if user_uuid is not None:
            # user configuration
            is_valid = check_uuid(server_uuid)
            if not is_valid:
                error = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR.message
                error_code = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR
                developer_message = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp

            try:
                vpnserverconfig = vpnserverconfig_db.find_user_config()
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
                vpnserverconfig = vpnserverconfig_db.find_by_server_uuid()
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
