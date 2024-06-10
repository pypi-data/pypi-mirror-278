from flask import render_template
from markdown import Markdown

from cbr_website_beta.data.odin.Analysis__Chat_Threads import Analysis__Chat_Threads

HTML_TITLE__ALL_CHAT_THREADS = 'All Chat Threads'

class Odin__Panels__Chat_Threads:

    def exposed_methods(self):
        return { 'all_chat_threads': self.all_chat_threads ,
                 'chat_thread'     : self.chat_thread      }

    def all_chat_threads(self):
        return render_template(**self.all_chat_threads__kwargs())

    def all_chat_threads__kwargs(self):
        chat_threads = Analysis__Chat_Threads(max_answer_size=200)
        users_threads = chat_threads.users__consolidated_threads()
        return  { "template_name_or_list" : "dev/chat_threads/all_threads.html" ,
                  "title"                 : HTML_TITLE__ALL_CHAT_THREADS        ,
                  'users_threads'         : users_threads                       }

    def chat_thread(self, thread_id):
        chat_threads = Analysis__Chat_Threads(max_answer_size=0)
        thread_data = chat_threads.create_consolidated_thread(thread_id)
        kwargs      = dict(thread_id=thread_id, thread_data=thread_data)
        return render_template(**self.chat_thread__kwargs(**kwargs))

    def chat_thread__kwargs(self, **kwargs):
        return  { "template_name_or_list" : "dev/chat_threads/dev-thread-view.html" ,
                  "title"                 : HTML_TITLE__ALL_CHAT_THREADS            ,
                  **kwargs}

