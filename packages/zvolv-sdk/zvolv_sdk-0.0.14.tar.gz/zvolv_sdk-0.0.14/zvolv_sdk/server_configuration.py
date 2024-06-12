import os
from dotenv import load_dotenv

class EnvVariables(object):
    if(os.path.exists("../../.env")):
        load_dotenv()
    
    @staticmethod
    def get_val(key):
        try:
            return os.environ[key]
        except KeyError:
            raise Exception(f"error {key} variable not found in env")

    @staticmethod
    def get_zvolv_localhost_url():
        return EnvVariables.get_val('LOCALHOST_URL')

    @staticmethod
    def get_api_base_url():
        return EnvVariables.get_val('BASE_URL')

    @staticmethod
    def get_api_version():
        return EnvVariables.get_val('API_VERSION')

    @staticmethod
    def get_api_17_version():
        return EnvVariables.get_val('API_VERSION_17')

    @staticmethod
    def get_zvolv_user_id():
        return EnvVariables.get_val('ADMIN_EMAIL')

    @staticmethod
    def get_zvolv_password():
        return EnvVariables.get_val('ADMIN_PASSWORD')

    @staticmethod
    def get_business_tag_id():
        return EnvVariables.get_val('BUSINESS_TAG_ID')

    @staticmethod
    def get_zvolv_domain():
        return EnvVariables.get_val('BUSINESS_DOMAIN')