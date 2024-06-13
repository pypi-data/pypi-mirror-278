from flask import request, g

from cbr_website_beta.flask.Flask_Utils import Flask_Utils

MAX_COOKIE_SIZE = 25

#@xray_trace("add_cookies_to_g")
def add_cookies_to_g():
    if Flask_Utils.is_static_request():
        return
    cookie_dict = {}
    session_id = None
    for key, value in request.cookies.items():
        if len(value) > MAX_COOKIE_SIZE:
            formatted_value = f"{value[:MAX_COOKIE_SIZE]} - size: {len(value)}"
        else:
            formatted_value = value

        cookie_dict[key] = formatted_value
        if key == 'CBR_TOKEN':
            session_id = value

    g.cookies    = cookie_dict
    g.session_id = session_id