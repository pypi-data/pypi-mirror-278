from flask                                       import request, g, render_template
from flask                                       import current_app
from cbr_website_beta.flask.Flask_Utils          import Flask_Utils
from cbr_website_beta.flask.filters.Current_User import g_user_data, g_user_data_current_username

BYPASS_AUTH              = False

#@xray_trace("allow_anonymous")
def allow_anonymous():
    if Flask_Utils.is_static_request():                                             # no checks for static requests
        return

    auth_data = { "allow"                   : False       ,
                  "bypass_auth"             : BYPASS_AUTH ,
                  "redirect_to"             : None        ,
                  "current_user"            : None        ,
                  "static_path"             : False       ,
                  "view_function"           : None        ,
                  "function_allow_anonymous": None        }

    view_function = current_app.view_functions.get(request.endpoint)

    if view_function:
        auth_data["function_allow_anonymous"] = hasattr(view_function, '_allow_anonymous')
        if auth_data["function_allow_anonymous"]:
            auth_data['allow'] = True

    auth_data['current_user'] = g_user_data_current_username()
    if BYPASS_AUTH or auth_data['current_user']:
        auth_data['allow'] = True

    g.auth_data = auth_data
    if auth_data['allow']:
        return
    else:
        #return redirect(auth_data['redirect_to'])
        return render_template('home/accounts/unauthorized.html')

# #@xray_trace("admin_only")
# def allow_users():                              # todo: implement logic
#     user_data = Current_User().user_data()
#     return

def admins_only():
    if Flask_Utils.is_static_request():
        return
    #user_data = Current_User().user_data()
    user_data     = g_user_data()
    view_function = current_app.view_functions.get(request.endpoint)

    if view_function:
        if hasattr(view_function, '_admins_only'):
            if 'CBR-Team' not in user_data.get('cognito:groups', []):
                return render_template('home/accounts/unauthorized.html')