import logging
import os
import sys

from flask import Flask

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
from api import register_api

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load config based on env variable
ENVIRONMENT_CONFIG = os.environ.get("ENVIRONMENT_CONFIG", default='DevelopmentConfig')
app.config.from_object("%s.%s" % ('config', ENVIRONMENT_CONFIG))

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
