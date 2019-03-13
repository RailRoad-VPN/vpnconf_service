import logging
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import *
from app.model.vpn.server import VPNServerDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import check_uuid
from response import make_api_response, make_error_request_response, check_required_api_fields
from api import ResourceAPI, APIResourceURL
from response import APIResponseStatus, APIResponse


class VPNSServersAPI(ResourceAPI):
    __version__ = 1

    logger = logging.getLogger(__name__)

    __endpoint_name__ = __qualname__
    __api_url__ = 'vpns/servers'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, VPNSServersAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<string:suuid>', methods=['GET', 'PUT'])
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, *args) -> None:
        super().__init__(*args)
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=VPNCError.REQUEST_NO_JSON)

        ip = request_json.get(VPNServerDB._ip_field, None)
        hostname = request_json.get(VPNServerDB._hostname_field, None)
        port = request_json.get(VPNServerDB._port_field, None)
        condition_version = request_json.get(VPNServerDB._condition_version_field, None)
        type_id = request_json.get(VPNServerDB._type_id_field, None)
        status_id = request_json.get(VPNServerDB._status_id_field, None)
        bandwidth = request_json.get(VPNServerDB._bandwidth_field, None)
        load = request_json.get(VPNServerDB._load_field, None)
        geo_position_id = request_json.get(VPNServerDB._geo_position_id_field, None)

        req_fields = {
            'ip': ip,
            'hostname': hostname,
            'port': port,
            'type_id': type_id,
            'status_id': status_id,
            'bandwidth': bandwidth,
            'load': load,
            'geo_position_id': geo_position_id,
        }

        error_fields = check_required_api_fields(fields=req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        vpnserver_db = VPNServerDB(storage_service=self.__db_storage_service, port=port, ip=ip, hostname=hostname,
                                   condition_version=condition_version, type_id=type_id, status_id=status_id,
                                   bandwidth=bandwidth, load=load, geo_position_id=geo_position_id)

        try:
            suuid = vpnserver_db.create()
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

        if request_json is None:
            return make_error_request_response(http_code=HTTPStatus.BAD_REQUEST, err=VPNCError.REQUEST_NO_JSON)

        vpnserver_uuid = request_json.get(VPNServerDB._suuid_field, None)

        is_valid_suuid = check_uuid(suuid)
        is_valid_vpnserver_uuid = check_uuid(vpnserver_uuid)
        if not is_valid_suuid or not is_valid_vpnserver_uuid or suuid != vpnserver_uuid:
            return make_error_request_response(http_code=HTTPStatus.BAD_REQUEST,
                                               err=VPNCError.VPNSERVER_IDENTIFIER_ERROR)

        ip = request_json.get(VPNServerDB._ip_field, None)
        hostname = request_json.get(VPNServerDB._hostname_field, None)
        port = request_json.get(VPNServerDB._port_field, None)
        condition_version = request_json.get(VPNServerDB._condition_version_field, None)
        type_id = request_json.get(VPNServerDB._type_id_field, None)
        status_id = request_json.get(VPNServerDB._status_id_field, None)
        bandwidth = request_json.get(VPNServerDB._bandwidth_field, None)
        load = request_json.get(VPNServerDB._load_field, None)
        geo_position_id = request_json.get(VPNServerDB._geo_position_id_field, None)

        req_fields = {
            'ip': ip,
            'hostname': hostname,
            'port': port,
            'condition_version': condition_version,
            'type_id': type_id,
            'status_id': status_id,
            'bandwidth': bandwidth,
            'load': load,
            'geo_position_id': geo_position_id,
        }

        error_fields = check_required_api_fields(fields=req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        vpnserver_db = VPNServerDB(storage_service=self.__db_storage_service, suuid=suuid, ip=ip, port=port,
                                   hostname=hostname, condition_version=condition_version, type_id=type_id,
                                   status_id=status_id, bandwidth=bandwidth, load=load, geo_position_id=geo_position_id)

        try:
            self.logger.debug('do update VPN server')
            vpnserver_db.update()
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

    def get(self, suuid: str = None) -> Response:
        super(VPNSServersAPI, self).get(req=request)

        type_id = request.args.get("type_id", None)
        status_id = request.args.get("status_id", None)

        vpnserver_db = VPNServerDB(storage_service=self.__db_storage_service, suuid=suuid, type_id=type_id,
                                   status_id=status_id, limit=self.pagination.limit, offset=self.pagination.offset)
        if suuid is not None:
            is_valid = check_uuid(suuid)
            if not is_valid:
                error = VPNCError.VPNSERVER_IDENTIFIER_ERROR.message
                error_code = VPNCError.VPNSERVER_IDENTIFIER_ERROR.code
                developer_message = VPNCError.VPNSERVER_IDENTIFIER_ERROR.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp

            try:
                vpnserver = vpnserver_db.find_by_suuid()
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
                                        data=vpnserver.to_api_dict())
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
        else:
            # list of all servers (but with specific type_id or status_id (if exists)
            try:
                vpnserver_list = vpnserver_db.find()
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

            vpnservers_dict = [vpnserver_list[i].to_api_dict() for i in range(0, len(vpnserver_list))]
            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                        data=vpnservers_dict, limit=self.pagination.limit,
                                        offset=self.pagination.offset)
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)

        return resp
