import logging
from pprint import pprint

from flask import Flask

from app.common.psql_helper import PostgreSQL
from app.common.storage import DBStorageService

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load the default configuration
app.config.from_object('config.DevelopmentConfig')

with app.app_context():
    psql = PostgreSQL(app=app)

db_storage_service = DBStorageService(psql=psql)
