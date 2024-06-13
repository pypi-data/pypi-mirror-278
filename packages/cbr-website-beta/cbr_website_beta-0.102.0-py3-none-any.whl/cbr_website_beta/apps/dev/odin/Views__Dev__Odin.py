from flask import render_template

from cbr_website_beta.apps.odin.S3_Backend_Analysis import S3_Backend_Analysis
from osbot_utils.testing.Duration import Duration


HTML_TITLE_ODIN_ACTIONS = 'Odin Actions'

class Views__Dev__Odin:

    def __init__(self):
        self.s3_backend_analysis = S3_Backend_Analysis()

    def api_update_s3_data(self, update_sessions=True, update_users=True):
        with Duration(print_result=False) as duration_update_db_sessions:
            if update_sessions:
                self.s3_backend_analysis.s3_update_db_sessions_status()
        with Duration(print_result=False) as duration_update_users:
            if update_users:
                self.s3_backend_analysis.s3_update_db_users_metadata()
        result = {'duration_update_sessions': round(duration_update_db_sessions.seconds(),2),
                  'duration_update_users'   : round(duration_update_users      .seconds(),2)}
        return result

    def odin_actions(self):
        return render_template(**self.odin_actions__render_config())

    def odin_actions__render_config(self):
        return { "template_name_or_list" : "dev/odin_actions.html" ,
                 "title"                 : HTML_TITLE_ODIN_ACTIONS }