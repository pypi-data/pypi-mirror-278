# import osbot_llms
# from osbot_utils.utils.Files import path_combine, file_contents
#
#
# class API_OSBot_LLMs:
#
#     def path_osbot_llms(self):
#         return osbot_llms.path
#
#     def path_version_file(self):
#         return path_combine(self.path_osbot_llms(), 'version')
#
#     def path_web_static(self):
#         return path_combine(self.path_osbot_llms(), 'web_static/src')
#
#     def url_path_chatbot_js(self):
#         return '/llms-ui/chatbot_openai/Chatbot_OpenAI.js'
#
#     def version(self):
#         return file_contents(self.path_version_file()).strip()