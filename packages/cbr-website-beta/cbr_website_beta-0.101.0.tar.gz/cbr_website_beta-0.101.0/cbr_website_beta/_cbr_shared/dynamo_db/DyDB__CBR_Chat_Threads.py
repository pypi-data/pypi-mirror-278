import traceback

from cbr_website_beta._cbr_shared.schemas.CBR_Logging import CBR_Logging
from cbr_website_beta.apps.CBR_Config import cbr_config
from cbr_website_beta.utils.Web_Utils import Web_Utils
from osbot_aws.aws.dynamo_db.domains.DyDB__Table_With_Timestamp import DyDB__Table_With_Timestamp
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import date_time_now

DYNAMO_DB__TABLE_NAME__CHAT_THREADS = '{env}__cbr_chat_threads'


class DyDB__CBR_Chat_Threads(DyDB__Table_With_Timestamp):

    env: str = cbr_config.env()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_name    = DYNAMO_DB__TABLE_NAME__CHAT_THREADS.format(env=self.env)
        self.disabled      = cbr_config.aws_enabled()

    def date_today(self):
        return date_time_now(date_time_format='%Y-%m-%d')

    def documents__today(self):
        if self.disabled:
            return []
        index_name  = 'date'
        index_type  = 'S'
        index_value = date_time_now(date_time_format='%Y-%m-%d')
        documents = self.query_index(index_name=index_name, index_type=index_type, index_value=index_value)
        return documents



dydb_cbr_chat_threads = DyDB__CBR_Chat_Threads()
