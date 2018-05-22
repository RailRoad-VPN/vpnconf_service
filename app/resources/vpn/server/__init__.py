import json
import logging
import sys
import uuid
from http import HTTPStatus

from flask import Response, request, make_response

from app.exception import *
from app.model.vpn.server import VPNServerDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import JSONDecimalEncoder, check_uuid
from api import ResourceAPI
from response import APIResponseStatus, APIResponse


class VPNServerAPI(ResourceAPI):
    __version__ = 1

    __api_url__ = 'vpns/servers'

    _config = None

    __db_storage_service = None

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        if request_json is None:
            error=VPNCError.REQUEST_NO_JSON.phrase
            error_code = VPNCError.REQUEST_NO_JSON
            developer_message = VPNCError.REQUEST_NO_JSON.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_response(json.dumps(response_data.serialize()), http_code)

        version = request_json.get(VPNServerDB._version_field, None)
        state_version = request_json.get(VPNServerDB._state_version_field, None)
        type_id = request_json.get(VPNServerDB._type_id_field, None)
        status_id = request_json.get(VPNServerDB._status_id_field, None)
        bandwidth = request_json.get(VPNServerDB._bandwidth_field, None)
        load = request_json.get(VPNServerDB._load_field, None)
        geo_position_id = request_json.get(VPNServerDB._geo_position_id_field, None)

        vpnserver_db = VPNServerDB(storage_service=self.__db_storage_service, version=version,
                                   state_version=state_version, type_id=type_id, status_id=status_id,
                                   bandwidth=bandwidth, load=load, geo_position_id=geo_position_id)

        try:
            suuid = vpnserver_db.create()
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_response(json.dumps(response_data.serialize()), http_code)

        resp = make_response('', HTTPStatus.CREATED)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], self.__api_url__, suuid)
        return resp

    def put(self, suuid: str) -> Response:
        request_json = request.json

        if request_json is None:
            error=VPNCError.REQUEST_NO_JSON.phrase
            error_code = VPNCError.REQUEST_NO_JSON
            developer_message = VPNCError.REQUEST_NO_JSON.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_response(json.dumps(response_data.serialize()), http_code)

        vpnserver_suuid = request_json.get(VPNServerDB._suuid_field, None)

        is_valid_suuid = check_uuid(suuid)
        is_valid_vpnserver_suuid = check_uuid(vpnserver_suuid)
        if not is_valid_suuid or not is_valid_vpnserver_suuid:
            error = VPNCError.VPNSERVER_IDENTIFIER_ERROR.phrase
            error_code = VPNCError.VPNSERVER_IDENTIFIER_ERROR
            developer_message = VPNCError.VPNSERVER_IDENTIFIER_ERROR.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_response(json.dumps(response_data.serialize()), http_code)
            return resp

        if suuid != vpnserver_suuid:
            error = VPNCError.VPNSERVER_IDENTIFIER_ERROR.phrase
            error_code = VPNCError.VPNSERVER_IDENTIFIER_ERROR
            developer_message = VPNCError.VPNSERVER_IDENTIFIER_ERROR.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_response(json.dumps(response_data.serialize()), http_code)
            return resp

        version = request_json.get(VPNServerDB._version_field, None)
        state_version = request_json.get(VPNServerDB._state_version_field, None)
        type_id = request_json.get(VPNServerDB._type_id_field, None)
        status_id = request_json.get(VPNServerDB._status_id_field, None)
        bandwidth = request_json.get(VPNServerDB._bandwidth_field, None)
        load = request_json.get(VPNServerDB._load_field, None)
        geo_position_id = request_json.get(VPNServerDB._geo_position_id_field, None)

        vpnserver_db = VPNServerDB(storage_service=self.__db_storage_service, suuid=suuid, version=version,
                                   state_version=state_version, type_id=type_id, status_id=status_id,
                                   bandwidth=bandwidth, load=load, geo_position_id=geo_position_id)

        try:
            vpnserver_db.update()
        except VPNException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_response(json.dumps(response_data.serialize()), http_code)

        resp = make_response('', HTTPStatus.OK)
        return resp

    def get(self, suuid: str = None) -> Response:
        if suuid is not None:
            is_valid = check_uuid(suuid)
            if not is_valid:
                error = VPNCError.VPNSERVER_IDENTIFIER_ERROR.phrase
                error_code = VPNCError.VPNSERVER_IDENTIFIER_ERROR
                developer_message = VPNCError.VPNSERVER_IDENTIFIER_ERROR.description
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_response(json.dumps(response_data.serialize()), http_code)
                return resp

            vpnserver_db = VPNServerDB(storage_service=self.__db_storage_service, suuid=suuid)

            try:
                vpnserver = vpnserver_db.find_by_suuid()
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
                                        data=vpnserver.to_dict())
            resp = make_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)
        else:
            vpnserver_db = VPNServerDB(storage_service=self.__db_storage_service)

            try:
                vpnserver_list = vpnserver_db.find()
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

            vpnservers_dict = [vpnserver_list[i].to_dict() for i in range(0, len(vpnserver_list))]
            response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK, data=vpnservers_dict)
            resp = make_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)

        return resp
