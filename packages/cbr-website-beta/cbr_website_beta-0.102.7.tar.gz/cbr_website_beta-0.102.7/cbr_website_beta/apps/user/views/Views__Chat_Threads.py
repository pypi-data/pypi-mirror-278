from flask import render_template

from cbr_website_beta.data.odin.Analysis__Chat_Threads import Analysis__Chat_Threads
from cbr_website_beta.flask.filters.Current_User import g_user_data_current_username


HTML_TITLE__USER_CHAT_THREAD = 'User Chat Thread'

class Views__Chat_Threads:

    def __init__(self):
        self.analysis__chat_threads = Analysis__Chat_Threads()

    def chat_thread(self,thread_id):
        chat_threads  = Analysis__Chat_Threads(max_answer_size=0)
        thread_data   = chat_threads.create_consolidated_thread(thread_id)
        kwargs        = dict(thread_id=thread_id, thread_data=thread_data)
        render_kwargs =   { "template_name_or_list" : "user/chat/user-thread-view.html" ,
                            "title"                 : HTML_TITLE__USER_CHAT_THREAD      ,
                            **kwargs                                                    }
        return render_template(**render_kwargs)

    def chat_threads(self):
        user = g_user_data_current_username()
        if user:
            threads_data = self.analysis__chat_threads.threads_data__by_user(user)
            return render_template('user/chat/user-threads.html', threads_data=threads_data)
