# from os import environ
#
# from cbr_website_beta.llms.API_Open_AI import API_Open_AI
# from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
# from osbot_utils.decorators.methods.cache_on_self import cache_on_self
# from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
# from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Json import Sqlite__DB__Json
# from osbot_utils.utils.Dev import pprint
# from osbot_utils.utils.Files import current_temp_folder, path_combine
# from osbot_utils.utils.Json import json_dump, json_dumps, json_loads
# from osbot_utils.utils.Misc import str_sha256, timestamp_utc_now
#
# ENV_NAME_PATH_LOCAL_DBS      = 'PATH_LOCAL_DBS'
# DB_NAME                      = 'open_ai_cache.sqlite'
# TABLE_NAME__OPEN_AI_REQUESTS = 'open_ai_requests'
#
# class Table__Open_AI__Requests(Kwargs_To_Self):
#     request_data  : str
#     request_hash  : str
#     response_data : str
#     response_hash : str
#     timestamp     : int
#     comment       : str
#
# class Open_AI__Cache:
#     #sqlite_db_json : Sqlite__DB__Json
#     sqlite_database: Sqlite__Database
#
#     def __init__(self) -> None:
#         self.sqlite_database = Sqlite__Database(db_path=self.path_db())
#
#     @cache_on_self
#     def api_open_ai(self):
#         return API_Open_AI()
#
#     def cached_data(self, **kwargs):
#         table = self.table_open_ai_requests()
#         request_data = json_dump(kwargs)
#         request_hash = str_sha256(request_data)
#         cached_data = table.select_row_where(request_hash=request_hash)
#         return cached_data
#
#     def cached_response(self, **kwargs):
#         cached_data = self.cached_data(**kwargs)
#         if cached_data:
#             response_data_str = cached_data.get('response_data')
#             response_data = json_loads(response_data_str)
#             return response_data
#         return None
#
#     def call_api_open_ai__create(self,**kwargs):   # messages, model=None, temperature=None, seed=None, max_tokens=None
#         return self.api_open_ai().create(**kwargs)
#
#     def call_chat_completion_create(self, **kwargs):
#         table = self.table_open_ai_requests()
#         cached_data = self.cached_data(**kwargs)
#         if cached_data:
#             response_data_str = cached_data.get('response_data')
#             response_data     = json_loads(response_data_str)
#         else:
#             request_data = json_dump(kwargs)                            # todo refactor this code so that we don't have to calculate this twice
#             request_hash = str_sha256(request_data)
#             chunks = []
#             response_data_stream = self.call_api_open_ai__create(**kwargs)
#             for chunk in response_data_stream:
#                 if chunk:
#                     chunks.append(chunk)
#             response_data = json_dumps(chunks)
#             response_hash = str_sha256(response_data)
#             row_data = { 'comment'      : ''                 ,
#                          'request_data'  : request_data       ,
#                          'request_hash'  : request_hash       ,
#                          'response_data' : response_data      ,
#                          'response_hash' : response_hash      ,
#                          'timestamp'     : timestamp_utc_now()}
#             table.add_row_and_commit(**row_data)                                # add to cache
#
#
#         return response_data
#
#     def path_db_folder(self):
#         return environ.get(ENV_NAME_PATH_LOCAL_DBS) or current_temp_folder()
#
#     def path_db(self):
#         return path_combine(self.path_db_folder(), DB_NAME)
#
#     def table_open_ai_requests(self):
#         table = self.sqlite_database.table(TABLE_NAME__OPEN_AI_REQUESTS)
#         table.row_schema = Table__Open_AI__Requests
#         if table.not_exists():
#             table.create()
#         return table
