import os
from functools import cache

from flask import Flask
from importlib import import_module
from flask_minify import Minify

from cbr_website_beta.flask.Flask_Utils                 import FLASK_APP__STATIC_PATH, FLASK_APP__STATIC_URL
from cbr_website_beta.flask.filters.Athena_Html_Content import Athena_Html_Content
from cbr_website_beta.flask.filters.Current_User        import Current_User
from cbr_website_beta.flask.filters.Misc_Filters        import Misc_Filters
from cbr_website_beta.flask.filters.Obj_Data            import Obj_Data
from cbr_website_beta.flask.filters.Pretty_Json         import Pretty_Json
from cbr_website_beta.flask.register_error_handling     import register_error_handling
from cbr_website_beta.flask.register_hooks              import register_hooks
from cbr_website_beta.flask.register_logging            import register_logging
from cbr_website_beta.flask.register_logging_in_g       import register_logging_in_g
from cbr_website_beta.flask.register_middlewares        import register_middlewares
from cbr_website_beta.flask.register_processors         import register_processors
from cbr_website_beta import static
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self

def register_blueprints(app):
    blueprints = ['api', 'llms', 'root' ,'dev', 'home', 'minerva', 'user']
    for module_name in blueprints:
        full_module_name = f'cbr_website_beta.apps.{module_name}.{module_name}_routes'
        module = import_module(full_module_name)
        app.register_blueprint(module.blueprint)

def flask_app_kwargs():
    return dict(static_folder   = FLASK_APP__STATIC_PATH ,
                static_url_path = FLASK_APP__STATIC_URL  )

def create_flask_app():
    app_kwargs = flask_app_kwargs()
    app = Flask(__name__, **app_kwargs)
    return app

def create_app(config):                         # todo: refactor to class
    app = create_flask_app()
    register_error_handling(app)
    register_middlewares   (app)
    app.config.from_object (config)
    register_blueprints    (app)
    register_processors    (app)
    register_hooks         (app)
    register_logging       (app)
    register_logging_in_g  (app)


    app.template_folder = '../apps/templates'
    return app






class Flask_Site:

    def __init__(self):
        pass

    @cache
    def app(self):
        app_config = self.app_config()
        app        = create_app(app_config)
        self.setup(app)
        if not self.debug():
            Minify(app=app, html=True, js=False, cssless=False)
        return app

    def app_config(self):
        from cbr_website_beta.apps.config import config_dict
        return config_dict[self.get_config_mode().capitalize()]


    def debug(self):
        return (os.getenv('DEBUG', 'False') == 'True')

    def get_config_mode(self):
        return 'Debug' if self.debug() else 'Production'

    def setup(self, app):
        self.register_filters(app)

    def register_filters(self, app):
        Athena_Html_Content (app)
        Current_User        (app)
        Pretty_Json         (app)
        Obj_Data            (app)
        Misc_Filters        (app)
