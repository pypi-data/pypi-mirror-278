from cbr_website_beta.flask.hooks import allow_anonymous


def disable_bypass_auth():                          # todo: remove once login bug is fixed
    allow_anonymous.BYPASS_AUTH = False