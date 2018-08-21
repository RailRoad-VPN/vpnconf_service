import logging
import os
import sys
from http import HTTPStatus

from flask import Flask, request

from app.resources.geos import GeosAPI
from app.resources.geos.cities import GeosCitiesAPI
from app.resources.geos.countries import GeosCountriesAPI
from app.resources.geos.states import GeosStatesAPI
from app.resources.vpns.device_platforms import VPNSDevicePlatformsAPI
from app.resources.vpns.mgmt.users import VPNSMGMTUsersAPI
from app.resources.vpns.mgmt.vpns.servers.connections import MGMTVPNSServersConnections
from app.resources.vpns.servers import VPNSServersAPI
from app.resources.vpns.servers.config_templates import VPNSConfigTemplatesAPI
from app.resources.vpns.servers.configurations import VPNSServersConfigurationsAPI
from app.resources.vpns.servers.connections import VPNSServersConnectionsAPI
from app.resources.vpns.servers.meta import VPNServersMetaAPI
from app.resources.vpns.servers.statuses import VPNSServersStatusesAPI
from app.resources.vpns.types import VPNSTypesAPI
from app.service import AnsibleService

sys.path.insert(0, '../psql_library')
from psql_helper import PostgreSQL
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from response import make_error_request_response
from api import register_api

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load config based on env variable
ENVIRONMENT_CONFIG = os.environ.get("ENVIRONMENT_CONFIG", default='DevelopmentConfig')
logging.info("Got ENVIRONMENT_CONFIG variable: %s" % ENVIRONMENT_CONFIG)
config_name = "%s.%s" % ('config', ENVIRONMENT_CONFIG)
logging.info("Config name: %s" % config_name)
app.config.from_object(config_name)

with app.app_context():
    psql = PostgreSQL(app=app)

db_storage_service = DBStorageService(psql=psql)


app_config = app.config
api_base_uri = app_config['API_BASE_URI']

ansible_service = AnsibleService(ansible_inventory_file=app_config['ANSIBLE_CONFIG']['inventory_file'],
                                 ansible_path=app_config['ANSIBLE_CONFIG']['root_path'],
                                 ansible_playbook_path=app_config['ANSIBLE_CONFIG']['playbook_path'])

apis = [
    {'cls': VPNServersMetaAPI, 'args': [db_storage_service, app_config]},
    {'cls': VPNSServersAPI, 'args': [db_storage_service, app_config]},
    {'cls': VPNSServersConfigurationsAPI, 'args': [db_storage_service, app_config]},
    {'cls': VPNSServersConnectionsAPI, 'args': [db_storage_service, app_config]},
    {'cls': VPNSServersStatusesAPI, 'args': [db_storage_service, app_config]},
    {'cls': VPNSTypesAPI, 'args': [db_storage_service, app_config]},
    {'cls': VPNSDevicePlatformsAPI, 'args': [db_storage_service, app_config]},
    {'cls': VPNSConfigTemplatesAPI, 'args': [db_storage_service, app_config]},
    {'cls': GeosAPI, 'args': [db_storage_service, app_config]},
    {'cls': GeosCitiesAPI, 'args': [db_storage_service, app_config]},
    {'cls': GeosCountriesAPI, 'args': [db_storage_service, app_config]},
    {'cls': GeosStatesAPI, 'args': [db_storage_service, app_config]},
    {'cls': VPNSMGMTUsersAPI, 'args': [ansible_service, app_config]},
    {'cls': MGMTVPNSServersConnections, 'args': [ansible_service, app_config]},
]

register_api(app, api_base_uri, apis)


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
           request.accept_mimetypes['text/html']


@app.errorhandler(400)
def not_found_error(error):
    return make_error_request_response(HTTPStatus.BAD_REQUEST)


@app.errorhandler(404)
def not_found_error(error):
    return make_error_request_response(HTTPStatus.NOT_FOUND)


@app.errorhandler(500)
def internal_error(error):
    return make_error_request_response(HTTPStatus.INTERNAL_SERVER_ERROR)
