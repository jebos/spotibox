import logging.config

import os

from flask import Flask, Blueprint
from box_rest_api import settings
from box_rest_api.api.box.endpoints.rfid_uri_mapping import ns as rfid_uri_namespace
from box_rest_api.api.restplus import api
from box_rest_api.database import db, reset_database

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

def configure_app(flask_app):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(rfid_uri_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)
    if settings.SQLALCHEMY_DATABASE_RESET:
        with flask_app.app_context():
            reset_database()

def main():
    initialize_app(app)
    app.run(debug=settings.FLASK_DEBUG, host=settings.FLASK_SERVER_NAME, port=settings.FLASK_SERVER_PORT)


if __name__ == "__main__":
    main()
