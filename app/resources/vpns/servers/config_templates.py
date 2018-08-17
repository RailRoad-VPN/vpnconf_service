import logging
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import *
from app.model.vpn.config_template import VPNServerConfigurationTemplateDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from response import make_api_response, make_error_request_response
from api import ResourceAPI
from response import APIResponseStatus, APIResponse
from rest import APIResourceURL


class VPNSConfigTemplatesAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = __qualname__
    __api_url__ = 'vpns/config_templates'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, VPNSConfigTemplatesAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<string:conf_template_uuid>', methods=['GET'])
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        resp = make_error_request_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def put(self, suuid: str) -> Response:
        resp = make_error_request_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def get(self, conf_template_uuid: str = None) -> Response:
        super(VPNSConfigTemplatesAPI, self).get(req=request)

        type_id = request.args.get('type_id', None)
        platform_id = request.args.get('platform_id', None)

        vpnserverconfigtempl_db = VPNServerConfigurationTemplateDB(storage_service=self.__db_storage_service,
                                                                   suuid=conf_template_uuid,
                                                                   vpn_type_id=type_id,
                                                                   vpn_device_platform_id=platform_id,
                                                                   limit=self.pagination.limit,
                                                                   offset=self.pagination.offset)
        if type_id is not None and platform_id is not None:
            try:
                vpnconfig_template_list = vpnserverconfigtempl_db.find_by_type_and_platform()
                vpnconfig_template_list_dict = [vpnconfig_template_list[i].to_api_dict() for i in
                                                range(0, len(vpnconfig_template_list))]
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=vpnconfig_template_list_dict)
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
        elif type_id is not None:
            try:
                vpnconfig_template_list = vpnserverconfigtempl_db.find_by_type()
                vpnconfig_template_list_dict = [vpnconfig_template_list[i].to_api_dict() for i in
                                                range(0, len(vpnconfig_template_list))]
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=vpnconfig_template_list_dict)
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
        elif platform_id is not None:
            try:
                vpnconfig_template_list = vpnserverconfigtempl_db.find_by_platform()
                vpnconfig_template_list_dict = [vpnconfig_template_list[i].to_api_dict() for i in
                                                range(0, len(vpnconfig_template_list))]
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=vpnconfig_template_list_dict)
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
        elif conf_template_uuid is not None:
            try:
                vpnconfig_template = vpnserverconfigtempl_db.find_by_suuid()
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=vpnconfig_template.to_api_dict())
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
            # all configuration templates
            try:
                vpnserverconfig_list = vpnserverconfigtempl_db.find()
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
