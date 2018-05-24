import logging
from pprint import pprint

import sys
from flask import Flask

from app.resources.geos import GeoAPI
from app.resources.geos.city import CityAPI
from app.resources.geos.country import CountryAPI
from app.resources.geos.state import StateAPI
from app.resources.vpns import VPNTypeAPI
from app.resources.vpns.servers import VPNServerAPI
from app.resources.vpns.servers.configuration import VPNServerConfigurationAPI
from app.resources.vpns.servers.meta import VPNServersMetaAPI
from app.resources.vpns.servers.status import VPNServerStatusAPI

sys.path.insert(0, '../psql_library')
from psql_helper import PostgreSQL
from storage_service import DBStorageService

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load the default configuration
app.config.from_object('config.DevelopmentConfig')

with app.app_context():
    psql = PostgreSQL(app=app)

db_storage_service = DBStorageService(psql=psql)

# VPN SERVERS META API
vpnserver_api_url = '%s/%s' % (app.config['API_BASE_URI'], VPNServersMetaAPI.__api_url__)
vpnserver_api_view_func = VPNServersMetaAPI.as_view('vpnserversmeta_api', db_storage_service, app.config)
app.add_url_rule(vpnserver_api_url, view_func=vpnserver_api_view_func, methods=['GET', 'POST', 'PUT'])

# VPN SERVERS API
vpnserver_api_url = '%s/%s' % (app.config['API_BASE_URI'], VPNServerAPI.__api_url__)
vpnserver_api_view_func = VPNServerAPI.as_view('vpnserver_api', db_storage_service, app.config)
app.add_url_rule(vpnserver_api_url, view_func=vpnserver_api_view_func, methods=['GET', 'POST', 'PUT'])
app.add_url_rule('%s/<string:suuid>' % vpnserver_api_url, view_func=vpnserver_api_view_func,
                 methods=['GET', 'POST', 'PUT'])

# VPN SERVER CONFIGURATIONS API
vpnserverconfig_api_url = '%s/%s' % (app.config['API_BASE_URI'], VPNServerConfigurationAPI.__api_url__)
vpnserverconfig_api_view_func = VPNServerConfigurationAPI.as_view('vpnserverconfig_api', db_storage_service, app.config)
app.add_url_rule(vpnserverconfig_api_url, view_func=vpnserverconfig_api_view_func, methods=['GET', 'POST', 'PUT'])

# VPN SERVER STATUSES API
vpnserverstatus_api_url = '%s/%s' % (app.config['API_BASE_URI'], VPNServerStatusAPI.__api_url__)
vpnserverstatus_api_view_func = VPNServerStatusAPI.as_view('vpnserverstatus_api', db_storage_service, app.config)
app.add_url_rule(vpnserverstatus_api_url, view_func=vpnserverstatus_api_view_func, methods=['GET', 'POST', 'PUT'])
app.add_url_rule('%s/<int:sid>' % vpnserverstatus_api_url, view_func=vpnserverstatus_api_view_func,
                 methods=['GET', 'POST', 'PUT'])

# VPN TYPES API
vpntype_api_url = '%s/%s' % (app.config['API_BASE_URI'], VPNTypeAPI.__api_url__)
vpntype_api_view_func = VPNTypeAPI.as_view('vpntype_api', db_storage_service, app.config)
app.add_url_rule(vpntype_api_url, view_func=vpntype_api_view_func, methods=['GET', 'POST', 'PUT'])
app.add_url_rule('%s/<int:sid>' % vpntype_api_url, view_func=vpntype_api_view_func, methods=['GET', 'POST', 'PUT'])

# Geo Positions API
geoposition_api_url = '%s/%s' % (app.config['API_BASE_URI'], GeoAPI.__api_url__)
geoposition_api_view_func = GeoAPI.as_view('geopos_api', db_storage_service, app.config)
app.add_url_rule(geoposition_api_url, view_func=geoposition_api_view_func, methods=['GET', 'POST', 'PUT'])
app.add_url_rule('%s/<int:sid>' % geoposition_api_url, view_func=geoposition_api_view_func,
                 methods=['GET', 'POST', 'PUT'])

# Geo Position Cities API
geopositioncity_api_url = '%s/%s' % (app.config['API_BASE_URI'], CityAPI.__api_url__)
geopositioncity_api_view_func = CityAPI.as_view('geoposcity_api', db_storage_service, app.config)
app.add_url_rule(geopositioncity_api_url, view_func=geopositioncity_api_view_func, methods=['GET', 'POST', 'PUT'])
app.add_url_rule('%s/<int:sid>' % geopositioncity_api_url, view_func=geopositioncity_api_view_func,
                 methods=['GET', 'POST', 'PUT'])

# Geo Position Countries API
geopositioncountry_api_url = '%s/%s' % (app.config['API_BASE_URI'], CountryAPI.__api_url__)
geopositioncountry_api_view_func = CountryAPI.as_view('geoposcountry_api', db_storage_service, app.config)
app.add_url_rule(geopositioncountry_api_url, view_func=geopositioncountry_api_view_func, methods=['GET', 'POST', 'PUT'])
app.add_url_rule('%s/<string:code>' % geopositioncountry_api_url, view_func=geopositioncountry_api_view_func,
                 methods=['GET', 'POST', 'PUT'])

# Geo Position States API
geopositionstate_api_url = '%s/%s' % (app.config['API_BASE_URI'], StateAPI.__api_url__)
geopositionstate_api_view_func = StateAPI.as_view('geoposstate_api', db_storage_service, app.config)
app.add_url_rule(geopositionstate_api_url, view_func=geopositionstate_api_view_func, methods=['GET', 'POST', 'PUT'])
app.add_url_rule('%s/<string:code>' % geopositionstate_api_url, view_func=geopositionstate_api_view_func,
                 methods=['GET', 'POST', 'PUT'])


pprint(app.url_map._rules_by_endpoint)