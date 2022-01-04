import os
from configparser import ConfigParser

CONFIG_FILE = 'config.ini'

def get_root_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_config_path():
    return f"{get_root_path()}/configs/"    
    
def get_models_path():
    return f"{get_root_path()}/models/"
    
def get_schemas_path():
    return f"{get_root_path()}/schemas/"

CONFIGS = ConfigParser()
CONFIGS.read(get_config_path() + CONFIG_FILE)

def get_discogs_token():
    return CONFIGS['Credentials']['discogs_token']

def get_database():
    return get_config_path() + CONFIGS['Database']['db_file']

def get_table():
    return CONFIGS['Database']['table']
