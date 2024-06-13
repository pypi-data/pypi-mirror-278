# from osbot_aws.apis.Cloud_Watch import Cloud_Watch
# from osbot_utils.utils.Dev import pprint
#
#
# class Cloud_Watch_Metrics:
#     def __init__(self):
#         self.cloud_watch = Cloud_Watch()
#
#     def dashboard_widget(self, dashboard_name, widget_name):
#         widgets = self.dashboard_widgets(dashboard_name=dashboard_name)
#         return widgets.get(widget_name, {})
#
#     def dashboard_widgets(self, dashboard_name):
#         dashboard = self.cloud_watch.dashboard(dashboard_name=dashboard_name)
#         widgets = {}
#         for widget in dashboard.get('widgets'):
#             properties = widget.get('properties')
#             title      = properties.get('title')
#             widgets[title] = properties
#         return widgets
#
#     def dashboards(self):
#         return self.cloud_watch.dashboards()
#
#     def widget_screenshot(self, dashboard_name, widget_name, save_to_disk=False, start="-PT2H", end="P0D"):
#         widget_data = self.dashboard_widget(dashboard_name, widget_name)
#         widget_data['start' ] = start
#         widget_data['end'   ] = end
#         widget_data['period'] = 300
#         return self.cloud_watch.metric_widget_image(widget_data, save_to_disk=save_to_disk)
#
#     # def metric_list(self, namespace):
#     #     return self.cloud_watch.metric_list(namespace=namespace)
#     #
#     # def metric_statistics(self, namespace, metric_name, period, start_time, end_time, statistics):
#     #     return self.cloud_watch.metric_statistics(namespace=namespace, metric_name=metric_name, period=period, start_time=start_time, end_time=end_time, statistics=statistics)
#
