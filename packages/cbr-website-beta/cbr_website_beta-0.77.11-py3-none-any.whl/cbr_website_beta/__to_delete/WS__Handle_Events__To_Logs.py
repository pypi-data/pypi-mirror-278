# import json
#
# from cbr_website_beta._cbr_shared.dynamo_db.DyDB__CBR_Logging       import dydb_cbr_logging
#
# from cbr_website_beta.aws.apigateway.web_sockets.WS__Handle_Lambda  import WS__Handle_Lambda
# from cbr_website_beta.utils.Site_Utils                              import Site_Utils
# from osbot_utils.utils.Misc                                         import wait_for
#
#
# class WS__Handle_Events__To_Logs(WS__Handle_Lambda):
#     site_utils : Site_Utils
#     version    : str
#     def __init__(self):
#         super().__init__()
#         self.version = self.site_utils.version()
#
#     def route__connect(self, event, connection_id):
#         self.send_message(f'Connect requested', connection_id, event)
#         return super().route__connect(event, connection_id)
#
#     def route_disconnect(self, event, connection_id):
#         self.send_message(f'Disconnect requested', connection_id, event)
#         return super().route_disconnect(event, connection_id)
#
#     def route_default(self, event, connection_id):
#         body = event.get('body', 'NA')
#         self.send_message     (f'Default route reached with connection ID', connection_id, event)
#         self.sent_message_back('on DEFAULT', connection_id, body)
#         return super().route_default(event, connection_id)
#
#     def route_unknown(self, event, connection_id, route_key):
#         self.send_message(f'Unknown routeKey:' + route_key, connection_id, event)
#         return super().route_unknown(event, connection_id, route_key)
#
#     def send_message(self, route_key, ws_connection_id, event):
#         message = f'[{self.version}] ws message "{route_key}" with connection id: {ws_connection_id}'
#         kwargs = dict(message    = message        ,
#                       extra_data = {'event': event})
#         dydb_cbr_logging.add_log_message(**kwargs)
#
#
#     def sent_message_back(self, event, connection_id, body):
#         try:
#             apiId = 'ow2twc6ee4'
#             region = 'eu-west-2'
#             stage = 'prod'
#             endpoint_url = f'https://{apiId}.execute-api.{region}.amazonaws.com/{stage}'
#
#             import boto3
#             client = boto3.client('apigatewaymanagementapi',
#                                   endpoint_url=endpoint_url)
#             wait_for(2)
#             reply_data = {'message': 'CCCCC Hi: ', 'event': event, "body": body}
#             client.post_to_connection(ConnectionId=connection_id, Data=json.dumps(reply_data))
#             kwargs = dict(message=f'sent message back to client : {reply_data}', extra_data=reply_data)
#             dydb_cbr_logging.add_log_message(**kwargs)
#         except Exception as e:
#             kwargs = dict(message=f'error in sent_message_back: {e}')
#             dydb_cbr_logging.add_log_message(**kwargs)