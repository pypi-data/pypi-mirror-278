# from osbot_utils.utils.Dev import pprint
# from osbot_utils.utils.Json import json_dumps, json_loads
# from osbot_aws.apis.Logs import Logs
#
#
# class Cloud_Watch_Logs:
#
#     def __init__(self):
#         self.log_name          = 'cbr_website_beta.sep.2023'
#         self.stream_name__10_m = 'real_time_stream__10_minutes'
#         self.stream_name__1_h  = 'real_time_stream__1_hour'
#         self.logs__10_m        = Logs(group_name=self.log_name, stream_name=self.stream_name__10_m)
#         self.logs__1_h         = Logs(group_name=self.log_name, stream_name=self.stream_name__1_h )
#         try:
#             self.logs__10_m.create()
#             self.logs__1_h .create()
#         except Exception as error:
#             pprint(f'**** Error in Cloud_Watch_Logs: {error}' )
#
#     def send_log(self, log_data):
#         log_data['via'] = 'Cloud_Watch_Logs'
#         message = json_dumps(log_data)
#
#         result__10m = self.logs__10_m.event_add(message)    # todo: fix stream , since at the moment it is not deleting data after 10m
#         #result__1h  = self.logs__1_h .event_add(message)   # for now we only send to the 10m stream
#         return dict(result__10m=result__10m)#, result__1h=result__1h)
#
#     def get_logs(self, logs, limit=10000, hours=24):              # 10000 is the maximum allowed by AWS (or 1M)
#         messages = logs.messages(limit=limit, hours=hours)
#
#         log_data = []
#         for message in messages:
#             log_data.append(json_loads(message))
#         return log_data
#
#     def get_logs__10_m(self, limit=10000, hours=1):
#         return self.get_logs(self.logs__10_m, limit, hours=hours)
#
#     def get_logs__1_h(self, count=10000):
#         return self.get_logs(self.logs__1_h, count)