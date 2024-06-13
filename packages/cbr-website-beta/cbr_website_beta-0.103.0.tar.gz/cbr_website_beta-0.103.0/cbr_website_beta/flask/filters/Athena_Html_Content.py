from cbr_website_beta.apps.home.home_routes import dydb_cbr_logging
from cbr_website_beta.bots.Athena_Rest_API import Athena_Rest_API
from cbr_website_beta.utils.Markdown_Parser import Markdown_Parser
from osbot_utils.utils.Dev import pprint


class Athena_Html_Content:

    filter_name = 'athena_html_content'

    def __init__(self, app):
        app.jinja_env.filters[self.filter_name] = self.athena_html_content # todo: find a better way to register these filters

    def athena_html_content(self, path):
        try:
            athena_rest_api = Athena_Rest_API()
            content         = athena_rest_api.requests_get(path)
            return Markdown_Parser().content_to_html(content)
        except Exception as e:
            dydb_cbr_logging.log_exception(e)
            return "Error in loading athena content"
