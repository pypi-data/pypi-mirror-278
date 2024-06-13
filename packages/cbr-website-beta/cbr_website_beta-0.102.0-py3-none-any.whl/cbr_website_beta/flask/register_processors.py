from cbr_website_beta.flask.processors.date_time_now import date_time_now
from cbr_website_beta.flask.processors.menu_links import menu_links


def register_processors(app):

    @app.context_processor
    def inject__date_time_now():
        return {'date_time_now': date_time_now()}

    @app.context_processor
    def inject__menu_links():
        return { 'menu_links' : menu_links }