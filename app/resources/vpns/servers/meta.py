import json
import logging
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import *
from app.model.vpn.server.meta import VPNServersMetaDB
from rest import APIResourceURL

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import JSONDecimalEncoder, make_api_response
from api import ResourceAPI
from response import APIResponseStatus, APIResponse


class VPNServersMetaAPI(ResourceAPI):
    __version__ = 1

    __endpoint_name__ = 'VPNServersMetaAPI'
    __api_url__ = 'vpns/servers/meta'

    methods = ['GET', 'POST', 'PUT']

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, VPNServersMetaAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST'])
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        response_data = APIResponse(status=APIResponseStatus.failed.value, code=HTTPStatus.METHOD_NOT_ALLOWED,
                                    error=HTTPStatus.METHOD_NOT_ALLOWED.phrase,
                                    error_code=HTTPStatus.METHOD_NOT_ALLOWED)

        resp = make_api_response(json.dumps(response_data.serialize()), HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def put(self, sid: int) -> Response:
        response_data = APIResponse(status=APIResponseStatus.failed.value, code=HTTPStatus.METHOD_NOT_ALLOWED,
                                    error=HTTPStatus.METHOD_NOT_ALLOWED.phrase,
                                    error_code=HTTPStatus.METHOD_NOT_ALLOWED)

        resp = make_api_response(json.dumps(response_data.serialize()), HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def get(self) -> Response:
        super(VPNServersMetaAPI, self).get(req=request)

        vpnserversmeta_db = VPNServersMetaDB(storage_service=self.__db_storage_service, limit=self.pagination.limit,
                                             offset=self.pagination.offset)

        try:
            vpnserversmeta = vpnserversmeta_db.find()
        except VPNNotFoundException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.NOT_FOUND
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(json.dumps(response_data.serialize()), http_code)
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(json.dumps(response_data.serialize()), http_code)

        response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                    data=vpnserversmeta.to_api_dict(), limit=self.pagination.limit,
                                    offset=self.pagination.offset)
        resp = make_api_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)

        return resp
