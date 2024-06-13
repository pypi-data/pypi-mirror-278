import datetime
import json
import os
from pathlib import Path

import mysql.connector
from mysql.connector import Error

from shining_brain.config_loader import load_yaml, read_histories, write_histories
from shining_brain.database import CreateIndexStatement
from shining_brain.logger_setup import setup_logger
from shining_brain.util import generate_create_table_statement, generate_column_mapping, load_file_into_database, load_file_into_data_frame

log = setup_logger('ETL')


def execute_etl():
    for p in load_yaml():
        run_project(p)


def run_project(p):
    if p.enabled() is False:
        return
    create_database(p)
    (ddl, data) = extract_and_transform(p, Path(p.get_directory()))
    create_tables(ddl, p)
    modify_data(p, data)
    load_data(data, p)


def load_data(data, project):
    for key in data.keys():
        load_file_into_database(project, data[key]['data_frame'], key, data[key]['column_mapping'][key])


def create_tables(ddl, project):
    connection = create_connection_with_schema(project.get_database())
    try:
        cursor = connection.cursor()
        cursor.execute(ddl)
        log.info("Tables created successfully")
    except Error as e:
        log.error("Error while creating database: %s", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            log.info("MySQL connection is closed")


def update_value(df, column, rule):
    for index, row in df.iterrows():
        flag = True
        for v in rule.get_values():
            if v in row[column]:
                continue
            flag = False
        if flag is True:
            for result in rule.get_results():
                df.at[index, result.get_column()] = result.get_value()


def modify_data(project, data):
    if project.get_modifications() is None:
        return
    for modification in project.get_modifications():
        if modification.get_table() not in data:
            continue
        df = data[modification.get_table()]['data_frame']
        for column in modification.get_columns():
            for rule in column.get_rules():
                if rule.get_name() == 'contain':
                    update_value(df, column.get_name(), rule)


def extract_and_transform(project, data_path):
    log.info("Starting to extract data.")
    column_mapping = {}
    data = {}
    ddl = []
    histories = read_histories()
    for file_path in data_path.iterdir():
        filename = os.path.splitext(os.path.basename(file_path))[0]
        if not file_path.is_file():
            continue
        if filename in histories and histories.get(filename)['Last Modified'] == str(file_path.stat().st_mtime):
            continue

        histories[filename] = {
            'Project': str(project.get_name()),
            'Filename': str(file_path),
            'Last Modified': str(file_path.stat().st_mtime),
            'Size': str(file_path.stat().st_size),
            'Created At': str(datetime.datetime.now()),
            'Created By': 'System',
            'Updated At': str(datetime.datetime.now())
        }

        table_name = filename
        data_frame = load_file_into_data_frame(str(file_path))
        column_mapping[table_name] = generate_column_mapping(data_frame)
        data[table_name] = {'data_frame': data_frame, 'column_mapping': column_mapping}
        create_table_statement = generate_create_table_statement(data_frame.columns, column_mapping, table_name)

        ddl.append(create_table_statement)

        index_statements = get_index_statements(column_mapping, project, table_name)
        if index_statements is not None:
            ddl.extend(index_statements)

    write_histories(histories)
    ddl_statement = ';\n'.join(ddl)

    log.debug("Column Mapping:\n%s", json.dumps(column_mapping, sort_keys=True, indent=2))
    log.debug("DDL Statement: \n%s", ddl_statement)
    log.info("The data is extracted.")
    return ddl_statement, data


def get_index_statements(column_mapping, project, table_name):
    if project.get_indices() is  None:
        return None
    index_statements = []
    for index in project.get_indices():
        if table_name != index.get_table():
            continue
        for column in index.get_columns():
            column_name = column_mapping[index.get_table()][column]
            index_statements.append(CreateIndexStatement(table_name, column_name).get())
    return index_statements


def create_database(project):
    log.info("Starting to create schema.")
    connection = create_connection_without_schema(project)
    schema = project.get_database().get_schema()
    try:
        cursor = connection.cursor()
        cursor.execute(f'create schema if not exists {schema} default character set utf8mb4 collate utf8mb4_0900_ai_ci')
        log.info("Database created successfully")
    except Error:
        log.error("Error while creating database: ")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            log.info("MySQL connection is closed")
    log.info("Schema %s is created successfully.", schema)


def create_connection_without_schema(project):
    try:
        database = project.get_database()
        connection = mysql.connector.connect(
            host=database.get_host(),
            user=database.get_user(),
            password=database.get_password()
        )

        if connection.is_connected():
            log.info("Connected to database MySQL %s", connection.get_server_info())

    except Error:
        log.error("Error while connecting to database")
    return connection


def create_connection_with_schema(database):
    try:
        connection = mysql.connector.connect(
            host=database.get_host(),
            user=database.get_user(),
            password=database.get_password(),
            database=database.get_schema()
        )
        if connection.is_connected():
            log.info("Connected to database MySQL %s", connection.get_server_info())

    except Error:
        log.error("Error while connecting to database")
    return connection
