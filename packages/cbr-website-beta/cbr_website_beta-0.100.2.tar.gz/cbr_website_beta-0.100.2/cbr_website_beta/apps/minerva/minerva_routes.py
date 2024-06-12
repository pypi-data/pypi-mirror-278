from flask import render_template
from cbr_website_beta.apps.minerva import blueprint

EXPECTED_ROUTES__MINERVA = [ '/minerva', '/minerva/aws-costs']

# @blueprint.app_errorhandler(Exception)           # UndefinedError
# def handle_undefined_error(e):
#     error_details = {
#         "error_message": str(e),
#         "stack_trace": traceback.format_exc(),
#         # Add more context-specific data here if needed
#     }
#     return render_template('error_page.html'), 500

@blueprint.route('')
def minerva_root():
    return render_template('minerva/index.html')

# todo: fix this route when minerva is fixed (also add caching layer to minerva since there
#       is no point of making more than one call per 8 hours)
@blueprint.route('/aws-costs')
def aws_costs():
    # chart_data = Chart_Data__AWS__Minerva().aws_cost_explorer()
    # chart_labels = chart_data.get('all_days')
    # chart_series = chart_data.get('all_costs')
    # all_services = chart_data.get('all_services')
    chart_labels = {}
    chart_series = {}
    all_services = {}
    return render_template('minerva/aws-costs.html',
                           chart_labels=chart_labels,
                           chart_series=chart_series,
                           all_services=all_services)
