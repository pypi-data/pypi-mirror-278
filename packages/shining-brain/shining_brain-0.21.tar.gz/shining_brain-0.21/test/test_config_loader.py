from shining_brain.config_loader import load_yaml, read_histories, write_histories


def test_yaml():
    projects = load_yaml("application-test.yaml")

    assert projects is not None

    project = projects.pop(0)
    assert project.get_name() == 'p1'
    assert project.get_directory() == '~/p1'

    database = project.get_database()
    assert database is not None
    assert database.get_host() == '127.0.0.1'
    assert database.get_user() == 'test'
    assert database.get_password() == 'test'
    assert database.get_schema() == 'test'

    indices = project.get_indices()
    assert indices is not None

    index = indices.pop(0)
    assert index.get_table() == 't1'
    assert index.get_columns() == ['c1', 'c2']

    modifications = project.get_modifications()
    assert modifications is not None

    modification = modifications.pop(0)
    assert modification.get_table() == "t1"

    columns = modification.get_columns()
    assert columns is not None

    column = columns.pop(0)
    assert column.get_name() == 'c1'

    rules = column.get_rules()
    assert rules is not None

    rule = rules.pop(0)
    assert rule.get_name() == 'contain'
    assert rule.get_values() == ['v1', 'v2']

    results = rule.get_results()
    assert results is not None

    result = results.pop(0)
    assert result.get_column() == 'c1'
    assert result.get_value() == 'v3'


def test_reading_histories():
    print(read_histories()['a'])


def test_writing_histories():
    write_histories({"a": 1})
