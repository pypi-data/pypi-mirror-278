from flask import render_template, g
from cbr_website_beta.flask.filters.Current_User import Current_User


def view__tree_view():
    g.trace_call.trace_call_handler.stack.add_node(title='-- in view__tree_view')
    with g.trace_call:
        current_user = Current_User()
        current_user.user_data_from_s3()

    # view_model = g.trace_call.view_model
    # g.trace_call.print_traces()
    return render_template('dev/tree_view.html', title='Tree View')