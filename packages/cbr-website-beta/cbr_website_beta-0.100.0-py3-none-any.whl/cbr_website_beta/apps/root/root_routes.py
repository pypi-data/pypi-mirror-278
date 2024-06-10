from flask import render_template, redirect

from cbr_website_beta.apps.CBR_Config                   import cbr_config
from cbr_website_beta.apps.llms.Initial_Message         import Initial_Message
from cbr_website_beta.apps.llms.Prompt_Examples         import Prompt_Examples
from cbr_website_beta.apps.llms.System_Prompt           import System_Prompt
from cbr_website_beta.apps.llms.llms_routes             import user_data_for_prompt, current_user_data, target_athena_url
from cbr_website_beta.apps.root                         import blueprint
from cbr_website_beta.apps.user.user_profile            import render_page__login_required
from cbr_website_beta.flask.decorators.allow_annonymous import allow_anonymous
from cbr_website_beta.flask.utils.current_server        import current_server
from cbr_website_beta.utils.Site_Utils                  import Site_Utils
from cbr_website_beta.utils.Version import Version


@blueprint.route('/')
@allow_anonymous
def index():
    #if Current_User().is_logged_in():
        home_uri = f"{current_server()}home"
        return redirect(home_uri)
    #return render_template('home/accounts/login.html', segment='login')

@blueprint.route('/version')
@allow_anonymous
def version():
    return Version().value()

@blueprint.route('/home')
@blueprint.route('/home.html')
@allow_anonymous
def home():
    user_data       = current_user_data()
    title           = 'Welcome'
    first_name      = user_data.get('First name','')
    last_name       = user_data.get('Last name' ,'')
    content_view    = 'includes/home.html'

    template_name = '/pages/page_with_view.html'
    return render_template(template_name_or_list = template_name,
                           title                 =  title       ,
                           content_view          = content_view ,
                           first_name            = first_name   ,
                           last_name             = last_name    )

@blueprint.route('/athena')
@allow_anonymous
def athena():
    user_data = user_data_for_prompt()
    title     = 'Athena'
    if user_data or cbr_config.login_disabled():
        url_athena       = target_athena_url() + '/open_ai/prompt_with_system__stream'  # todo: refactor into helper method
        content_view     = '/llms/open_ai/chat_bot_ui.html'
        template_name    = '/pages/page_with_view.html'
        examples_title   = 'Prompt examples'

        return render_template( template_name_or_list = template_name               ,
                                content_view          = content_view                ,
                                examples_texts        = Prompt_Examples().athena()  ,        # todo: refactor to not need to call Prompt_Examples() on all calls
                                examples_title        = examples_title              ,
                                initial_message       = Initial_Message().athena()  ,         # todo: refactor to not need to call Prompt_Examples() on all calls
                                system_prompt         = System_Prompt().athena()    ,
                                title                 = title                       ,
                                url_athena            = url_athena                  ,
                                user_data             = user_data                   )
    else:
        return render_page__login_required(title)