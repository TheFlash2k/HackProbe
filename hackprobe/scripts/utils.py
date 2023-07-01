import configparser
from pymongo import MongoClient

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'

class Config:
    conn_string : str = ""
    db_name : str = ""
    collection_name : str = ""

def msg(_msg, mode='*', *args, **kwargs):
    _mode = { "+" : Colors.GREEN, "!" : Colors.RED, "?" : Colors.YELLOW, "*" : Colors.BLUE }
    print(f"[{_mode[mode]}{mode}{Colors.RESET}] {_msg}", *args, **kwargs)

def check_db():
    try:
        client = MongoClient(Config.conn_string)
        db = client[Config.db_name]
        collection = db[Config.collection_name]
        msg("Connected to the database.", '+')
        return True
    except Exception as e:
        msg(f"An error occurred! {e.__str__()}", '!')
        return None

def check_config(config_file='config.ini'):

    import os
    # If you people know any better way to do this, please let me know.
    if not os.path.exists(config_file):
        config_file = f"../{config_file}"
        if not os.path.exists(config_file):
            config_file = f"../../{config_file}"
            if not os.path.exists(config_file):
                msg("Config file not found.", '!')
                
    # Read absolute path of config file
    config_file = os.path.abspath(config_file)

    config = configparser.ConfigParser()
    config.read(config_file)
    msg(f"Loaded config file: {Colors.BLUE}{config_file}{Colors.RESET}", '*')
    if not config['DB-CONFIG']['conn_string'] or not config['DB-CONFIG']['db_name'] or not config['DB-CONFIG']['collection_name']:
        msg("Please configure the config.ini file first.", '!')

        if not config['DB-CONFIG']['conn_string']:
            msg("conn_string is not set.", '!')
        
        if not config['DB-CONFIG']['db_name']:
            msg("db_name is not set.", '!')
        
        if not config['DB-CONFIG']['collection_name']:
            msg("collection_name is not set.", '!')

        return False
    
    Config.conn_string = config['DB-CONFIG']['conn_string']
    Config.db_name = config['DB-CONFIG']['db_name']
    Config.collection_name = config['DB-CONFIG']['collection_name']

    msg("Config file is valid and variables have been set.", '+')
    msg(f"Connection String : {Colors.GREEN}{Config.conn_string}{Colors.RESET}", '*')
    msg(f"Database Name     : {Colors.GREEN}{Config.db_name}{Colors.RESET}", '*')
    msg(f"Collection Name   : {Colors.GREEN}{Config.collection_name}{Colors.RESET}", '*')

    msg("Checking database connection...", '*')
    if not check_db():
        msg("Please check your database connection.", '!')
    return True
