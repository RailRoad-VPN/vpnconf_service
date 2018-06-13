import logging
import os
import sys
from http import HTTPStatus

from flask import Flask, request

from app.resources.geos import GeoAPI
from app.resources.geos.city import CityAPI
from app.resources.geos.country import CountryAPI
from app.resources.geos.state import StateAPI
from app.resources.vpns import VPNTypeAPI
from app.resources.vpns.servers import VPNServerAPI
from app.resources.vpns.servers.configurations import VPNServerConfigurationAPI
from app.resources.vpns.servers.meta import VPNServersMetaAPI
from app.resources.vpns.servers.status import VPNServerStatusAPI

sys.path.insert(0, '../psql_library')
from psql_helper import PostgreSQL
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import make_error_request_response
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

apis = [
    {'cls': VPNServersMetaAPI, 'args': [db_storage_service, app_config]},
    {'cls': VPNServerAPI, 'args': [db_storage_service, app_config]},
    {'cls': VPNServerConfigurationAPI, 'args': [db_storage_service, app_config]},
    {'cls': VPNServerStatusAPI, 'args': [db_storage_service, app_config]},
    {'cls': VPNTypeAPI, 'args': [db_storage_service, app_config]},
    {'cls': GeoAPI, 'args': [db_storage_service, app_config]},
    {'cls': CityAPI, 'args': [db_storage_service, app_config]},
    {'cls': CountryAPI, 'args': [db_storage_service, app_config]},
    {'cls': StateAPI, 'args': [db_storage_service, app_config]},
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
