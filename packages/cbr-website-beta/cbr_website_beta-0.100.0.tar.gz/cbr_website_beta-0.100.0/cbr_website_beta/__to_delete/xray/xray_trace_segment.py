# import functools
# import sys
# #from aws_xray_sdk.core import patch_all, xray_recorder
# from cbr_website_beta.flask.middleware.xray_middleware import current_segment_save_to, current_segment_print
#
#
# def xray_trace_segment(name="Xray Test", print_traces=False, save_json_to=None):
#
#     def decorator(f):
#         @functools.wraps(f)
#         def wrapper(*args, **kwargs):
#             subsegment = xray_recorder.begin_segment(name)
#             patch_all()
#             try:
#                 result = f(*args, **kwargs)
#             except Exception as e:
#                 exc_type, exc_value, exc_traceback = sys.exc_info()
#                 subsegment.add_exception(exc_value, exc_traceback)
#                 raise
#             finally:
#                 if save_json_to:
#                     current_segment_save_to(save_json_to)
#                 if print_traces:
#                     current_segment_print()
#                 xray_recorder.end_segment()
#             return result
#         return wrapper
#     return decorator