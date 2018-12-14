import logging
import traceback

from flask_restplus import Api
from box_rest_api import settings
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Box REST API', description='')

@api.errorhandler
def default_error_handler(e):
    message = 'Wupps an unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'No result from Database.'}, 404
