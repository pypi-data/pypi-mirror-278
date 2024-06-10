from cbr_website_beta._testing.test_utils.TestCase__CBR__Website import TestCase__CBR__Website


class CBR__API_Pages(TestCase__CBR__Website):

    # API pages
    def api_user_data(self): return self.open_json('/api/user-data')