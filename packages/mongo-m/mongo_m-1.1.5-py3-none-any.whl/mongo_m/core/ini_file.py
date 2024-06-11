import configparser
import os

__all__ = ['create_file_ini', 'get_config']

FILE = f"{os.getcwd()}/migration/config.ini"


def create_file_ini():
    """
    Creates a new INI file with default settings for MongoDB.

    This function creates a new INI file with default settings for MongoDB. The INI file is used to store configuration
    information for the MongoDB database. The function does the following:

    1. Creates a new instance of the `configparser.ConfigParser` class.
    2. Sets the default values for the MongoDB configuration parameters in the `config` object.
    3. Opens the INI file specified by the `FILE` variable in write mode.
    4. Writes the contents of the `config` object to the INI file.
    5. Closes the INI file.

    Parameters:
    None

    Returns:
    None
    """
    config = configparser.ConfigParser()
    config['MONGO'] = {
        'host': 'localhost',
        'port': 27020,
        'user': 'devUser',
        'password': 'nbgfre736251',
        'database': 'queue_service',
        'module_path': 'migration'
    }
    with open(FILE, 'w') as f:
        config.write(f)


def get_config() -> configparser.ConfigParser:
    """
    Reads the configuration file specified by the `FILE` variable and returns a `configparser.ConfigParser` object.

    Returns:
        configparser.ConfigParser: A `configparser.ConfigParser` object containing the parsed configuration data.
    """
    config = configparser.ConfigParser()
    config.read(FILE)
    return config
