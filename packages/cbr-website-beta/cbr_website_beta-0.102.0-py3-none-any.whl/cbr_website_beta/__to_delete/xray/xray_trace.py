# from functools import wraps
# from cbr_website_beta.flask.middleware.xray_middleware import current_segment_print
# from cbr_website_beta.utils.Web_Utils import Web_Utils
#
# def xray_trace(name):
#     if Web_Utils.running_in_aws() is False:                 # only enable this decorator when running in AEWS
#         return lambda f: f
#     def decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             subsegment = xray_recorder.begin_subsegment(name)
#             if subsegment:
#                 subsegment.put_http_meta ('url'       , name    )       # this is a hack to add the name to the box that shows in the
#                 subsegment.put_http_meta ('method'    , ''      )       #     xray UI (makes is easier to find the function)
#                 subsegment.put_annotation('trace_name', name    )
#                 #subsegment.put_metadata  ('operation' , name    )
#             try:
#                 result = f(*args, **kwargs)
#             except Exception as e:
#                 subsegment.add_exception(e)
#                 raise
#             finally:
#                 xray_recorder.end_subsegment()
#             return result
#         return wrapper
#     return decorator
#
# from aws_xray_sdk.core import xray_recorder
#
# class XRay_Trace:
#     def __init__(self, name='XRay_Trace', source='pytest', print_segment=False):
#         self.name          = name
#         self.source        = source
#         self.print_segment = print_segment
#
#     def __enter__(self):
#         #if self.skip_pytest_check:
#         self.subsegment = xray_recorder.begin_subsegment(self.name)
#         if self.subsegment:
#             self.subsegment.put_http_meta('url'        , self.name)  # to show name in the x-ray UI
#             self.subsegment.put_http_meta('method'     , ''       )      # placeholder, can be left empty
#             self.subsegment.put_annotation('source'    , self.source)
#             #self.subsegment.put_annotation('annotation', self.name)
#
#     def __exit__(self, exc_type, exc_value, traceback):
#         if self.subsegment:
#             if exc_type is not None:
#                 self.subsegment.add_exception(exc_value, traceback)
#             xray_recorder.end_subsegment()
#         if self.print_segment:
#             current_segment_print()