from functools import cache

from markdown import Markdown

from cbr_website_beta.aws.s3.DB_Odin_Data import DB_Odin_Data
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Lists import list_index_by, list_group_by
from osbot_utils.utils.Misc import list_set, timestamp_to_str_date, timestamp_to_str_time

DEFAULT_MAX_ANSWER_SIZE = 100

class Analysis__Chat_Threads(Kwargs_To_Self):
    db_odin_data    : DB_Odin_Data
    max_answer_size : int = DEFAULT_MAX_ANSWER_SIZE
    markdown_answer = True


    def all_consolidated_threads(self):
        results = {}
        for thread_id in self.threads_ids():
            results[thread_id] = self.create_consolidated_thread(thread_id)
        return results

    # def threads_ids_per_user(self):
    #     results = {}
    #     for thread_id, threads_data in self.threads_data__by_id().items():
    #         user = threads_data[0].get('user')
    #         results[user] = results.get(user, []) + [thread_id]
    #     return []


    def create_consolidated_thread(self, thread_id):
        by_thread_id = self.threads_data__by_id()
        thread_data = by_thread_id.get(thread_id)
        thread_data = sorted(thread_data, key=lambda x: x['chat_thread']['index'], reverse=False)

        self.remove_system_prompts(thread_data)
        self.add_index_to_root   (thread_data)

        combined_data = []

        # Use a range with a step of 2 since data is in pairs
        for i in range(0, len(thread_data), 2):
            prompt_entry       = thread_data[i]                                               # Assuming the prompt is always followed by its corresponding answer
            answer_entry       = thread_data[i + 1] if i + 1 < len(thread_data) else {}
            index              = prompt_entry.get('index')                                           # Extract index from the prompt entry
            user               = prompt_entry.get('user')
            user_prompt        = self.get_user_prompt(prompt_entry)
            answer             = self.get_answer     (answer_entry)
            answer_size        = self.get_answer_size(answer_entry)
            prompt_timestamp   = int(prompt_entry.get('chat_thread', {}).get('timestamp',0))
            prompt_date        = timestamp_to_str_date(prompt_timestamp, date_format='%d %b')
            prompt_time        = timestamp_to_str_time(prompt_timestamp)
            answer_timestamp   = int(answer_entry.get('chat_thread', {}).get('timestamp', 0))
            prompt_with_images = len(prompt_entry.get('chat_thread', {}).get('data', {}).get('images', [])) > 0
            prompt_model       = prompt_entry.get('chat_thread', {}).get('data', {}).get('model' , '')

            timespan = (answer_timestamp - prompt_timestamp) / 1000
            combined_entry = {  'index'             : index              ,
                                'prompt'            : user_prompt        ,
                                'prompt_date'       : prompt_date        ,
                                'prompt_time'       : prompt_time        ,
                                'prompt_timestamp'  : prompt_timestamp   ,
                                'prompt_with_images': prompt_with_images ,
                                'prompt_model'      : prompt_model       ,
                                'answer'            : answer             ,
                                'answer_size'       : answer_size        ,
                                'answer_timestamp'  : answer_timestamp   ,
                                'user'              : user               ,
                                'timespan'          : timespan           }

            combined_data.append(combined_entry)
        return combined_data

    def get_user_prompt(self, entry):
        chat_thread = entry.get('chat_thread', {})
        data        = chat_thread.get('data', {})
        return data.get('user_prompt', 'NA')

    def get_answer(self, entry):
        max_answer_size = self.max_answer_size
        answer_raw_data = self.get_answer_raw_data(entry)
        if max_answer_size:
            if len(answer_raw_data) > max_answer_size:
                return answer_raw_data[:max_answer_size] + " ...."
            return answer_raw_data[:max_answer_size]
        if self.markdown_answer:
            return self.markdown().convert(source=answer_raw_data)                   # todo: security: review for XSS injection via Markdown payloads
        return answer_raw_data

    def get_answer_raw_data(self, entry):
        chat_thread     = entry.get('chat_thread', {})
        answer_raw_data = chat_thread.get('answer', '')
        return answer_raw_data

    def get_answer_size(self, entry):
        return len(self.get_answer_raw_data(entry))


    # def get_histories(self, entry):
    #     chat_thread = entry.get('chat_thread', {})
    #     data       = chat_thread.get('data', {})
    #     return data.get('histories', '')


    def add_index_to_root(self, threads_data):
        for item in threads_data:
            chat_thread = item.get('chat_thread',{})
            index       = int(chat_thread.get('index'))
            item['index'] = index

    @cache_on_self
    def markdown(self):
        return Markdown(extensions=['tables'])

    def remove_system_prompts(self, threads_data):
        for item in threads_data:
            self.remove_system_prompt(item)

    def remove_system_prompt(self, item):
        chat_thread = item.get('chat_thread',{})
        data        = chat_thread.get('data', {})
        if 'system_prompts' in data:
            del data['system_prompts']

    @cache_on_self
    def threads_data(self):
        return self.db_odin_data.chat_threads()

    def threads_data__by_id(self):
        return list_group_by(self.threads_data(), 'thread_id')

    def threads_data__by_user(self, user):
        return self.user__consolidated_threads(user)

    def threads_ids(self):
        return list_set(self.threads_data__by_id())

    def user__consolidated_threads(self, user):
        return self.users__consolidated_threads().get(user, {})

    def users__consolidated_threads(self):
        results = {}
        for thread_id, consolidated_thread in self.all_consolidated_threads().items():
            user = consolidated_thread[0].get('user')
            results[user] = results.get(user, {})
            results[user][thread_id] = consolidated_thread
        return results


