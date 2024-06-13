# import inspect
# from os import environ
# from unittest import TestCase
#
# import pytest
# from dotenv import load_dotenv
#
# from cbr_website_beta.llms.Open_AI__Cache import Open_AI__Cache, ENV_NAME_PATH_LOCAL_DBS, \
#     TABLE_NAME__OPEN_AI_REQUESTS
# from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
# from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
# from osbot_utils.utils.Dev import pprint
# from osbot_utils.utils.Files import current_temp_folder
# from osbot_utils.utils.Misc import word_wrap
#
#
# class test_Open_AI__Cache(TestCase):
#     open_api_cache  : Open_AI__Cache
#     sqlite_database : Sqlite__Database
#
#     @classmethod
#     def setUpClass(cls):
#         load_dotenv()
#         cls.open_api_cache = Open_AI__Cache()
#         cls.sqlite_database = cls.open_api_cache.sqlite_database
#
#     def test__setup__(self):
#         assert self.open_api_cache.sqlite_database.in_memory is False
#
#     def test_call_api_open_ai__create(self):
#         question = 'just say 42'
#         messages = [{"role": "user", "content": question}]
#         kwargs = dict(messages=messages)
#         response = self.open_api_cache.call_api_open_ai__create(**kwargs)
#         assert inspect.isgenerator(response)
#         assert '42' in list(response)
#
#     @pytest.mark.skip('todo: fix text to use similar cache as the one uses in AWS Bedrock')
#     def test_call_chat_completion_create(self):
#         prompts = ['just say 42', '42', 'what is 42', 'what is your GenAI base model',
#                    'what is a CISO', 'What is DORA in cyber Security',
#                    'what is the current day',
#                    'can you count to 10',
#                    'what do you know about me?',
#                    'as a board member, what questions should I ask my CISO?',
#                    'can you write a letter from a board member to a CISO asking what is the current risk profile?']
#         for prompt in prompts:
#             messages = [{"role": "user", "content": prompt}]
#             kwargs = dict(messages=messages)
#             response = self.open_api_cache.call_chat_completion_create(**kwargs)
#             cached_response = self.open_api_cache.cached_response(**kwargs)
#             assert response == cached_response
#             #print(word_wrap(''.join(response),length=70))
#
#     def test_path_db_folder(self):
#         path_path_db_folder = self.open_api_cache.path_db_folder()
#         expected_path       = environ.get(ENV_NAME_PATH_LOCAL_DBS) or current_temp_folder()
#         assert path_path_db_folder == expected_path
#
#     def test_table_open_ai_requests(self):
#         table = self.open_api_cache.table_open_ai_requests()
#         assert type(table)      is Sqlite__Table
#         assert table.exists()   is True
#         assert table.table_name == TABLE_NAME__OPEN_AI_REQUESTS
#         assert self.sqlite_database.exists() is True