# from functools import wraps
# from flask import redirect, url_for
#
# from flask import request
#
# from cbr_website_beta.apps.root import blueprint
# from cbr_website_beta.flask.filters.Current_User import Current_User, USER_DATA_WITH_NO_CBR_TOKEN
#
# def get_current_user_from_cookie():
#     return Current_User().current_user(context=None, field='username')
#
#
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         user = get_current_user_from_cookie()
#         if user is USER_DATA_WITH_NO_CBR_TOKEN:
#             return redirect(url_for('user_blueprint.unauthorized'))
#         return f(*args, **kwargs)
#     return decorated_function
