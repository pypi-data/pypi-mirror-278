from flask import g

from cbr_website_beta.apps.llms.llms_routes import current_user_data
from cbr_website_beta.flask.decorators.allow_annonymous import allow_anonymous
from cbr_website_beta.apps.api import blueprint
from cbr_website_beta.flask.filters.Current_User import Current_User, g_user_data

EXPECTED_ROUTES__API = ['/api/user-data']

@blueprint.route('/user-data')
@allow_anonymous
def user_data():
    return { "g.user_data": g_user_data()      ,
             "cognito"   : current_user_data() }
