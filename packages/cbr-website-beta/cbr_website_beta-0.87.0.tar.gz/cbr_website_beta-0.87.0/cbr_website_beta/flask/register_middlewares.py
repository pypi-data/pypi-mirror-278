from cbr_website_beta.flask.middleware.Fix_CloudFront_Domain import Fix_CloudFront_Domain
#from cbr_website_beta.flask.middleware.xray_middleware import xray_middleware


def register_middlewares(app):
    app.wsgi_app = Fix_CloudFront_Domain(app.wsgi_app)
    #xray_middleware(app)
