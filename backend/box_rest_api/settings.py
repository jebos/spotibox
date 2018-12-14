# Flask settings
FLASK_SERVER_NAME = 'localhost'
FLASK_SERVER_PORT = 5761
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_RESET = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
