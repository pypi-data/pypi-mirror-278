import pytest

from shining_brain.database import ColumnDefinition, CreateDefinition, CreateTableStatement


@pytest.mark.parametrize('datatype, length, default_value, is_null, expected', [
    ('varchar', 200, "Evan", True, 'varchar(200) null default "Evan"'),
    ('varchar', 200, None, True, 'varchar(200) null'),
    ('varchar', 200, "Evan", False, 'varchar(200) not null default "Evan"')
])
def test_column_definition(datatype, length, default_value, is_null, expected):
    column_definition = ColumnDefinition(datatype, length, default_value, is_null)
    assert column_definition.get() == expected


@pytest.mark.parametrize('column_name,, expected', [
    ('first_name', '`first_name` varchar(200) null'),
    ('middle_name', '`middle_name` varchar(200) null'),
    ('last_name', '`last_name` varchar(200) null')
])
def test_create_definition(column_name, expected):
    column_definition = ColumnDefinition()
    create_definition = CreateDefinition(column_name, column_definition)
    assert create_definition.get() == expected


@pytest.mark.parametrize('table_name, column_names, expected', [
    ('table_1', ['column_1'], 'drop table if exists table_1;\ncreate table table_1 (\n\t`column_1` varchar(200) null\n)'),
    ('table_2', ['column_1', 'column_2'], 'drop table if exists table_2;\ncreate table table_2 (\n\t`column_1` varchar(200) null,\n\t`column_2` varchar(200) null\n)')
])
def test_create_table_statement(table_name, column_names, expected):
    column_definition = ColumnDefinition()
    create_definitions = []
    for column_name in column_names:
        create_definitions.append(CreateDefinition(column_name, column_definition))
    statement = CreateTableStatement(table_name, create_definitions)
    assert statement.get() == expected
