import traceback

from flask import render_template, Flask

from cbr_website_beta._cbr_shared.dynamo_db.DyDB__CBR_Logging import DyDB__CBR_Logging
from cbr_website_beta.apps.CBR_Config import cbr_config
from cbr_website_beta.flask.decorators.allow_annonymous      import allow_anonymous



def register_error_handling(app: Flask):

    dydb_cbr_logging = DyDB__CBR_Logging()

    @app.errorhandler(Exception)
    def internal_server_error(exception):
        if cbr_config.dev__capture_exceptions():
            dydb_cbr_logging.log_exception(exception)
            return render_template('home/page-500.html', error=str(exception)), 500
        else:
            raise exception

    @app.route('/raise_exception')
    @allow_anonymous
    def cause_error():
        # This will cause an error and trigger the error handler
        return 1 / 0