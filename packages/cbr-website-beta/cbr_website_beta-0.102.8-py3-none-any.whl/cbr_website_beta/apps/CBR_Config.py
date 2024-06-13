import cbr_website_beta
from cbr_website_beta.utils.Version import version
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.utils.Status                       import status_ok, status_error
from osbot_utils.utils.Files import path_combine, folder_files, files_names
from osbot_utils.utils.Env import get_env, load_dotenv
from osbot_utils.base_classes.Type_Safe             import Type_Safe
from osbot_utils.utils.Toml                         import toml_dict_from_file

ENV_VAR_NAME__CBR_CONFIG_FILE     = 'CBR_CONFIG_FILE'
DEFAULT__CBR_CONFIG_FILE          = 'cbr-website.toml'      # default config mode which is the version that just has this site running locally
FOLDER__CBR_CONFIG_FILES          = './config'

DEFAULT__CBR_LOGO                 = 'cbr/cbr-logo-community.png'
DEFAULT__CONFIG_ASSETS_ROOT       = 'https://static.thecyberboardroom.com/assets'
DEFAULT__CONFIG_AWS_ENABLED       = False
DEFAULT__CONFIG_LOGIN_ENABLED     = False

class CBR_Config(Type_Safe):

    def __init__(self):
        super().__init__()
        load_dotenv()

    @cache_on_self
    def config(self):
        try:
            config_data = toml_dict_from_file(self.path_config_file())
            return status_ok(data=config_data)
        except Exception as error:
            return status_error(message='In CBR_Config failed to load config file', error=f'{error}', data={})

    def config_files(self):
        return files_names(folder_files(self.path_config_files(), pattern="*.toml"))

    def current_config_file_name(self):
        return get_env(ENV_VAR_NAME__CBR_CONFIG_FILE, DEFAULT__CBR_CONFIG_FILE)

    def path_config_file(self):
        return path_combine(self.path_config_files(), self.current_config_file_name())

    def path_config_files(self):
        return path_combine(cbr_website_beta.path, FOLDER__CBR_CONFIG_FILES)

    # top level sections

    def cbr_dev(self):
        return self.config().get('data',{}).get('cbr_dev', {})

    def cbr_website(self):
        return self.config().get('data',{}).get('cbr_website', {})

    # from env variables

    def env(self):
        return get_env('EXECUTION_ENV', 'LOCAL')


    # specific values

    def assets_dist(self):
        if self.env() == 'LOCAL':
            value = '/dist'
        else:
            value = f'https://static.thecyberboardroom.com/dist/{version}'
        return value

    def assets_root(self):
        return self.cbr_website().get('assets_root', DEFAULT__CONFIG_ASSETS_ROOT)

    def aws_enabled(self):
        return self.cbr_website().get('aws_enabled', DEFAULT__CONFIG_AWS_ENABLED)

    def aws_disabled(self):
        return self.aws_enabled() is False

    def cbr_logo(self):
        return self.cbr_website().get('cbr_logo', DEFAULT__CBR_LOGO)


    def dev__capture_exceptions(self):
        return self.cbr_dev().get('capture_exceptions', True)

    def login_enabled(self):
        return self.cbr_website().get('login_enabled', DEFAULT__CONFIG_LOGIN_ENABLED)

    def login_disabled(self):
        return self.login_enabled() is False

    # static values  # todo: figure out best place to store these, since they really shouldn't change
    def session_cookie_httponly(self):
        return True

    def remember_cookie_httponly(self):
        return True

    def remember_cookie_duration(self):
        return 3600                         # todo: look at increasing this value, since I think this is reason why the user session expires quite often

cbr_config = CBR_Config()
