# from unittest import TestCase
#
# from cbr_website_beta.llms.API_OSBot_LLMs import API_OSBot_LLMs
# from cbr_website_beta.utils._for_OSBot_Utils import parent_folder_name
# from osbot_playwright._extra_methdos_osbot import in_github_actions
# from osbot_utils.utils.Dev import pprint
#
# from osbot_utils.utils.Files import folder_exists, folder_name, file_exists, file_name, file_contents, path_combine
#
#
# class test_API_OSBot_LLMs(TestCase):
#
#     def setUp(self):
#         self.api_osbot_llms = API_OSBot_LLMs()
#
#     def test_path_osbot_llms(self):
#         path_to_osbot_llms = self.api_osbot_llms.path_osbot_llms()
#         assert folder_exists(path_to_osbot_llms)
#         assert folder_name(path_to_osbot_llms       ) == 'osbot_llms'
#         # if in_github_actions():
#         #     assert parent_folder_name(path_to_osbot_llms) == 'site-packages'
#         # else:
#         #     assert parent_folder_name(path_to_osbot_llms) == 'OSBot-LLMs'
#
#
#     def test_path_version_file(self):
#         version_file = self.api_osbot_llms.path_version_file()
#         assert file_exists(version_file)
#         assert file_name(version_file) == 'version'
#
#
#     def test_path_web_static(self):
#         path_web_static = self.api_osbot_llms.path_web_static()
#         assert folder_exists(path_web_static)
#         assert folder_name(path_web_static) == 'src'
#
#     def test_version(self):
#         version = self.api_osbot_llms.version()
#         assert version.startswith('v0') is True
#         assert version == file_contents(self.api_osbot_llms.path_version_file()).strip()
#
#     def test_url_path_chatbot_js(self):
#         url_path_chatbot_js  = self.api_osbot_llms.url_path_chatbot_js().replace('/llms-ui/', '')
#         path_web_static      = self.api_osbot_llms.path_web_static()
#         full_path_chatbot_js = path_combine(path_web_static, url_path_chatbot_js)
#         assert file_exists(full_path_chatbot_js)
#         assert "Chatbot_OpenAI.define()" in file_contents(full_path_chatbot_js)
#
#     # def test_chatbot_js_file(self):
#     #     chatbot_js_file = 'static/src/chatbot_openai/Chatbot_OpenAI.js'
