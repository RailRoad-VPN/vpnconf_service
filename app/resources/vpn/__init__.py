import json
import logging
import sys
from http import HTTPStatus

from flask import Response, make_response

from app.exception import *
from app.model.vpn import VPNTypeDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import JSONDecimalEncoder
from api import ResourceAPI
from response import APIResponseStatus, APIResponse


class VPNTypeAPI(ResourceAPI):
    __version__ = 1

    __api_url__ = 'vpns/types'

    _config = None

    __db_storage_service = None

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        response_data = APIResponse(status=APIResponseStatus.failed.value, code=HTTPStatus.METHOD_NOT_ALLOWED,
                                    error=HTTPStatus.METHOD_NOT_ALLOWED.phrase,
                                    error_code=HTTPStatus.METHOD_NOT_ALLOWED)

        resp = make_response(json.dumps(response_data.serialize()), HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def put(self, sid: int) -> Response:
        response_data = APIResponse(status=APIResponseStatus.failed.value, code=HTTPStatus.METHOD_NOT_ALLOWED,
                                    error=HTTPStatus.METHOD_NOT_ALLOWED.phrase,
                                    error_code=HTTPStatus.METHOD_NOT_ALLOWED)

        resp = make_response(json.dumps(response_data.serialize()), HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def get(self, sid: int = None) -> Response:
        if sid is not None:
            try:
                sid = int(sid)
            except ValueError:
                error = VPNCError.VPNTYPE_IDENTIFIER_ERROR.phrase
                error_code = VPNCError.VPNTYPE_IDENTIFIER_ERROR
                developer_message = VPNCError.VPNTYPE_IDENTIFIER_ERROR.description
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_response(json.dumps(response_data.serialize()), http_code)
                return resp

            vpntype_db = VPNTypeDB(storage_service=self.__db_storage_service, sid=sid)

            try:
                vpntype = vpntype_db.find_by_sid()
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_response(json.dumps(response_data.serialize()), http_code)
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_response(json.dumps(response_data.serialize()), http_code)

            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                        data=vpntype.to_dict())
            resp = make_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)
        else:
            vpntype_db = VPNTypeDB(storage_service=self.__db_storage_service)

            try:
                vpntype_list = vpntype_db.find()
            except VPNNotFoundException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.NOT_FOUND
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_response(json.dumps(response_data.serialize()), http_code)
            except VPNException as e:
                logging.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_response(json.dumps(response_data.serialize()), http_code)

            vpntype_dict = [vpntype_list[i].to_dict() for i in range(0, len(vpntype_list))]
            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                        data=vpntype_dict)
            resp = make_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)

        return resp