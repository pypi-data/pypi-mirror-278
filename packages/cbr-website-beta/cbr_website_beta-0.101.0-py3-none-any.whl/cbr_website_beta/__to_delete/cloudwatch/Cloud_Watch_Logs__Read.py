# from datetime import datetime, timedelta
#
# from osbot_utils.utils.Json import json_loads
#
# from osbot_utils.decorators.methods.cache_on_self import cache_on_self
#
# from osbot_aws.apis.Logs import Logs
# from typing import cast
#
# CBR_WEBSITE_LOG_GROUP_NAME = 'cbr_website_beta.flask.Flask_Site'
#
# class Cloud_Watch_Logs__Read:
#
#     @cache_on_self
#     def logs(self) -> Logs:
#         return Logs()
#
#     def log_groups(self):
#         logs = cast(Logs, self.logs())
#         return logs.groups_names()
#
#     def group_name(self):
#         return CBR_WEBSITE_LOG_GROUP_NAME
#
#     def generate_s3_keys(self, start_time, end_time, interval_minutes):
#         s3_keys = []
#         current_time = start_time - timedelta(minutes=start_time.minute % interval_minutes)
#         while current_time < end_time:
#             folder = current_time.strftime("%d/%m/%Y")
#             file_name = f"logs_{current_time.hour:02}_{current_time.minute:02}.json"
#             s3_keys.append(f"/{folder}/{file_name}")
#             current_time += timedelta(minutes=interval_minutes)
#         return s3_keys
#
#
#
#     def fetch_logs_from_cloudwatch(self, start_time, end_time):
#         cloudwatch = self.logs().client()
#         response = cloudwatch.filter_log_events(
#             logGroupName=self.group_name(),
#             startTime=start_time,
#             endTime=end_time
#         )
#
#         logs = []
#         for event in response["events"]:
#             logs.append(json_loads(event["message"]))
#
#         return logs