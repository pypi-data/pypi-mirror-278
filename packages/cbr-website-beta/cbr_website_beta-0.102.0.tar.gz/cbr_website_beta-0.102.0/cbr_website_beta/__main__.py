import os
import sys

def main():
    from cbr_website_beta.flask.Flask_Site import Flask_Site
    from osbot_utils.utils.Files import path_combine

    path_to_add = path_combine(__file__, '..')     # this is needed to that the apps folder can be resolved
    sys.path.append(path_to_add)

    flask_site = Flask_Site()
    app = flask_site.app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

if __name__ == "__main__":
    main()
