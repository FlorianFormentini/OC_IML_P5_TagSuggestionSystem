from flask import Blueprint, current_app
from flask_restx import Api, abort

from .utils import authorizations
from .tagsuggestion.tagsuggestion_endpoints import ns as tagsuggestion_ns

# API Blueprint declaration
api_blueprint = Blueprint('api', __name__)
api = Api(
    api_blueprint,
    authorizations=authorizations,
    title='OC P5 : StackOverflow Tag Suggestion System',
    version='1.0',
    description='Endpoints to use the different features'
)

# subscription to all namespaces
api.add_namespace(tagsuggestion_ns, path='/tagsuggestion')


@api.errorhandler
def default_error_handler(e):
    if not current_app.config['DEBUG']:
        abort(500, f'An unhandled exception occurred : {e}')
