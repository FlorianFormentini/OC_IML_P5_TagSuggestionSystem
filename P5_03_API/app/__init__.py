from flask import Flask

from .config import config_by_name


def create_app(config_name='dev') -> Flask:
    """Create and configure the app instance"""

    app = Flask(__name__, instance_relative_config=False, static_folder='./static')
    # load config
    app.config.from_object(config_by_name[config_name])

    with app.app_context():
        from .core.tagsuggestion_business import TransformTokenizer # noqa
        # import blueprints
        from .api import api_blueprint
        # register blueprints
        app.register_blueprint(api_blueprint)  # url_prefix='/api' to add a prefix
        return app
