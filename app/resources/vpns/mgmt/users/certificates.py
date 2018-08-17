import sys
from http import HTTPStatus
from typing import List

from flask import Response

from app.service import VPNMgmtService
from rest import APIResourceURL

sys.path.insert(0, '../rest_api_library')
from api import ResourceAPI
from response import APIResponseStatus, APIResponse, make_error_request_response
from response import make_api_response


class VPNSMgmtUsersCertsAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = __qualname__
    __api_url__ = 'vpns/mgmt/users/<string:user_uuid>/certificates'

    _config = None

    vpn_mgmt_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = f"{base_url}/{VPNSMgmtUsersCertsAPI.__api_url__}"
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['POST', 'DELETE']),
        ]
        return api_urls

    def __init__(self, vpn_mgmt_service: VPNMgmtService, config: dict) -> None:
        super().__init__()
        self._vpn_mgmt_service = vpn_mgmt_service
        self._config = config

    def post(self, user_uuid: str) -> Response:
        resp = make_error_request_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def put(self) -> Response:
        resp = make_error_request_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def get(self) -> Response:
        resp = make_error_request_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def delete(self, user_uuid: str):
        resp = make_error_request_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp
