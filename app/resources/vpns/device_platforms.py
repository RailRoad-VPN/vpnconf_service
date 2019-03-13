import logging
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import *
from app.model.vpn.device_platform import VPNDevicePlatformDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from response import make_api_response, make_error_request_response
from api import ResourceAPI, APIResourceURL
from response import APIResponseStatus, APIResponse


class VPNSDevicePlatformsAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = __qualname__
    __api_url__ = 'vpns/device_platforms'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, VPNSDevicePlatformsAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<int:sid>', methods=['GET', 'PUT']),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, *args) -> None:
        super().__init__(*args)
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        return make_error_request_response(HTTPStatus.METHOD_NOT_ALLOWED, err=VPNCError.METHOD_NOT_ALLOWED)

    def put(self, sid: int) -> Response:
        return make_error_request_response(HTTPStatus.METHOD_NOT_ALLOWED, err=VPNCError.METHOD_NOT_ALLOWED)

    def get(self, sid: int = None) -> Response:
        super(VPNSDevicePlatformsAPI, self).get(req=request)
        if sid is not None:
            try:
                sid = int(sid)
            except ValueError:
                return make_error_request_response(HTTPStatus.BAD_REQUEST,
                                                   err=VPNCError.VPN_DEVICE_PLATFORM_IDENTIFIER_ERROR)

            vpn_device_platform_db = VPNDevicePlatformDB(storage_service=self.__db_storage_service, sid=sid)

            try:
                vpntype = vpn_device_platform_db.find_by_sid()
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
                                        data=vpntype.to_api_dict())
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
        else:
            vpn_device_platform_db = VPNDevicePlatformDB(storage_service=self.__db_storage_service,
                                                         limit=self.pagination.limit, offset=self.pagination.offset)

            try:
                vpn_device_platform_list = vpn_device_platform_db.find()
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

            vpn_device_platform_dict = [vpn_device_platform_list[i].to_api_dict() for i in
                                        range(0, len(vpn_device_platform_list))]
            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                        data=vpn_device_platform_dict, limit=self.pagination.limit,
                                        offset=self.pagination.offset)
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)

        return resp
