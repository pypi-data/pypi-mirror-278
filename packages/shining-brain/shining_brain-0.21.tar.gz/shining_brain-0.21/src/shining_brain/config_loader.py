import json
import os
from json import JSONDecodeError
from pathlib import Path

import yaml

from shining_brain.logger_setup import setup_logger
from shining_brain.constants import work_directory

log = setup_logger('CONFIG_LOADER')

column_mapping_file = work_directory + os.sep + 'column_mapping.json'
data_path = Path(work_directory + os.sep + 'data')
ddl_file = work_directory + os.sep + 'ddl.sql'
application_config_file = work_directory + os.sep + 'application.yaml'
histories = work_directory + os.sep + 'histories.json'


class Result:
    def __init__(self, column=None, value=None):
        self.__column = column
        self.__value = value

    def get_column(self):
        return self.__column

    def get_value(self):
        return self.__value


class Rule:
    def __init__(self, name=None, values=None, results=None):
        self.__name = name
        self.__values = values

        if isinstance(results, list):
            self.__results = [Result(**item) for item in results]

    def get_name(self):
        return self.__name

    def get_values(self):
        return self.__values

    def get_results(self):
        return self.__results


class Column:
    def __init__(self, name=None, rules=None):
        self.__name = name

        if isinstance(rules, list):
            self.__rules = [Rule(**item) for item in rules]

    def get_name(self):
        return self.__name

    def get_rules(self):
        return self.__rules


class Modification:
    def __init__(self, table=None, columns=None):
        self.__table = table

        if isinstance(columns, list):
            self.__columns = [Column(**item) for item in columns]

    def get_table(self):
        return self.__table

    def get_columns(self):
        return self.__columns


class Index:
    def __init__(self, table=None, columns=None):
        self.__table = table
        self.__columns = columns

    def get_table(self):
        return self.__table

    def get_columns(self):
        return self.__columns


class Database:
    def __init__(self, host=None, user=None, password=None, schema=None):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__schema = schema

    def get_host(self):
        return self.__host

    def get_user(self):
        return self.__user

    def get_password(self):
        return self.__password

    def get_schema(self):
        return self.__schema


class Project:
    def __init__(self, name, enabled=False, directory=None, database=None, indices=None, modifications=None):
        self.__name = name
        self.__enabled = enabled
        self.__directory = directory
        self.__modifications = None
        self.__indices = None

        if isinstance(database, dict):
            self.__database = Database(**database)

        if isinstance(indices, list):
            self.__indices = [Index(**item) for item in indices]

        if isinstance(modifications, list):
            self.__modifications = [Modification(**item) for item in modifications]

    def get_name(self):
        return self.__name

    def enabled(self):
        return self.__enabled

    def get_directory(self):
        return self.__directory

    def get_database(self) -> Database:
        return self.__database

    def get_indices(self):
        return self.__indices

    def get_modifications(self):
        return self.__modifications


class Config:
    def __init__(self):
        pass

    @classmethod
    def load(cls, config):
        if not isinstance(config, dict):
            return None

        projects = config.get('projects')

        if not isinstance(projects, list):
            return None

        return [Project(**item) for item in projects]


def load_application_configuration():
    try:
        with open(application_config_file, 'r', encoding='UTF-8') as file:
            config = yaml.safe_load(file)
        if config is None or 'projects' not in config:
            raise ValueError('The application.yaml is empty. Please complete the basic configuration as outlined in '
                             'the accompanying document.')
        return config
    except FileNotFoundError as e:
        with open(application_config_file, 'x', encoding='UTF-8') as file:
            file.write('')
            raise ValueError('The application.yaml file has been created. Please complete the basic configuration as '
                             'outlined in the accompanying document.', e) from e


def load_column_mapping():
    try:
        with open(column_mapping_file, 'r', encoding='UTF-8') as file:
            if file.read(1):
                file.seek(0)
                return json.load(file)
    except JSONDecodeError:
        log.error("Invalid JSON in file.")
    except FileNotFoundError:
        log.error("File not found.")
    return {}


def read_histories():
    try:
        with open(histories, 'r', encoding='UTF-8') as file:
            if file.read(1):
                file.seek(0)
                return json.load(file)
    except JSONDecodeError as e:
        log.error(
            """
                Oops! It looks like there was an issue with parsing the JSON data. 
                This often happens when the JSON format is incorrect, such as a missing quotation mark, comma, or brace. 
                Please double-check the JSON structure to ensure it's correctly formatted and try again. 
                %s
            """, e)
    except FileNotFoundError:
        with open(histories, 'w', encoding='UTF-8') as file:
            file.write('')
        log.warning('File %s has been created.', histories)
    return {}


def write_histories(data):
    with open(histories, 'w', encoding='UTF-8') as file:
        return json.dump(data, file, indent=2, skipkeys=True)
    return {}


def load_yaml(config_file=application_config_file):
    try:
        with open(config_file, 'r', encoding='UTF-8') as file:
            config = yaml.safe_load(file)
        if config is None or 'projects' not in config:
            raise ValueError('The application.yaml is empty. Please complete the basic configuration as outlined in '
                             'the accompanying document.')

        return Config.load(config)
    except FileNotFoundError as e:
        with open(config_file, 'x', encoding='UTF-8') as file:
            file.write('')
            raise ValueError('The application.yaml file has been created. Please complete the basic configuration as '
                             'outlined in the accompanying document.', e) from e


application_config = load_application_configuration()
