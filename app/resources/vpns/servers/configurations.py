import json
import logging
import sys
import uuid
from http import HTTPStatus

from flask import Response, request

from app.exception import *
from app.model.vpn.server.configuration import VPNServerConfigurationDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import JSONDecimalEncoder, check_uuid, make_api_response
from api import ResourceAPI
from response import APIResponseStatus, APIResponse


class VPNServerConfigurationAPI(ResourceAPI):
    __version__ = 1

    __api_url__ = 'vpns/servers/<string:server_suuid>/configurations'

    _config = None

    __db_storage_service = None

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        user_suuid = request_json.get(VPNServerConfigurationDB._user_suuid_field, None)
        server_suuid = request_json.get(VPNServerConfigurationDB._server_suuid_field, None)
        file_path = request_json.get(VPNServerConfigurationDB._file_path_field, None)
        configuration = request_json.get(VPNServerConfigurationDB._configuration_field, None)

        vpnserverconfig_db = VPNServerConfigurationDB(storage_service=self.__db_storage_service, user_suuid=user_suuid,
                                                      server_suuid=server_suuid, file_path=file_path,
                                                      configuration=configuration)

        try:
            suuid = vpnserverconfig_db.create()
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
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], self.__api_url__, suuid)
        return resp

    def put(self, suuid: str) -> Response:
        request_json = request.json

        vpnserverconfig_suuid = request_json.get(VPNServerConfigurationDB._suuid_field, None)

        is_valid_suuid = check_uuid(suuid)
        is_valid_vpnserver_suuid = check_uuid(vpnserverconfig_suuid)
        if not is_valid_suuid or not is_valid_vpnserver_suuid:
            error = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR.phrase
            error_code = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR
            developer_message = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(json.dumps(response_data.serialize()), http_code)
            return resp

        if suuid != vpnserverconfig_suuid:
            error = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR.phrase
            error_code = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR
            developer_message = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(json.dumps(response_data.serialize()), http_code)
            return resp

        user_suuid = request_json.get(VPNServerConfigurationDB._user_suuid_field, None)
        server_suuid = request_json.get(VPNServerConfigurationDB._server_suuid_field, None)
        file_path = request_json.get(VPNServerConfigurationDB._file_path_field, None)
        configuration = request_json.get(VPNServerConfigurationDB._configuration_field, None)

        vpnserverconfig_db = VPNServerConfigurationDB(storage_service=self.__db_storage_service, suuid=suuid,
                                                      user_suuid=user_suuid, server_suuid=server_suuid,
                                                      file_path=file_path, configuration=configuration)

        try:
            vpnserverconfig_db.update()
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

    def get(self, server_suuid: str, user_suuid: str = None) -> Response:
        super(VPNServerConfigurationAPI, self).get(req=request)

        vpnserverconfig_db = VPNServerConfigurationDB(storage_service=self.__db_storage_service,
                                                      server_suuid=server_suuid, user_suuid=user_suuid)
        if user_suuid is not None:
            # user configuration
            is_valid = check_uuid(server_suuid)
            if not is_valid:
                error = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR.phrase
                error_code = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR
                developer_message = VPNCError.VPNSERVERCONFIG_IDENTIFIER_ERROR.description
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(json.dumps(response_data.serialize()), http_code)
                return resp

            try:
                vpnserverconfig = vpnserverconfig_db.find_user_config()
                response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                            data=vpnserverconfig.to_api_dict())
                resp = make_api_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)
                return resp
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(json.dumps(response_data.serialize()), http_code)
                return resp
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(json.dumps(response_data.serialize()), http_code)
                return resp
        else:
            # all server configurations
            try:
                vpnserverconfig = vpnserverconfig_db.find_by_server_suuid()
                response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                            data=vpnserverconfig.to_api_dict())
                resp = make_api_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)
                return resp
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(json.dumps(response_data.serialize()), http_code)
                return resp
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(json.dumps(response_data.serialize()), http_code)
                return resp
