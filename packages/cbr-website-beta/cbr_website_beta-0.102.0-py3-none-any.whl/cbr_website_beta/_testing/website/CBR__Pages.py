from cbr_website_beta._testing.test_utils.TestCase__CBR__Website import TestCase__CBR__Website
from cbr_website_beta.apps.home.home_routes import COGNITO_SIGN_IN


class CBR__Pages(TestCase__CBR__Website):

    # CBR Pages
    def athena   (self): return self.open('/athena'         )
    def content  (self): return self.open('/content'        )
    def login    (self): return self.open('/login'          )
    def home     (self): return self.open('/home'           )
    def videos   (self): return self.open('/content/videos' )




