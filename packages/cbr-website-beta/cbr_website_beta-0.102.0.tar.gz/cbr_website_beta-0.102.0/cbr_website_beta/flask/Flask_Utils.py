from flask import request

from cbr_website_beta           import static
from osbot_utils.utils.Files    import path_combine

FLASK_APP__STATIC_FOLDER    = 'dist'
FLASK_APP__STATIC_PATH      = path_combine(static.path, FLASK_APP__STATIC_FOLDER)
FLASK_APP__STATIC_URL       = f'/{FLASK_APP__STATIC_FOLDER}'
FLASK_APP__STATIC_RULE_NAME = f'/{FLASK_APP__STATIC_FOLDER}/<path:filename>'


class Flask_Utils:
    @staticmethod
    def is_static_request():
        return request.path.startswith(FLASK_APP__STATIC_URL)
