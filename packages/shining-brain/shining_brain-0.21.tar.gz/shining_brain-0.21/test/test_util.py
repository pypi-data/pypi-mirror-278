import os
import re
from io import BytesIO

import pandas as pd
import pytest

from shining_brain.constants import work_directory
from shining_brain.util import to_snake_case, extract_colored_rows, rename_columns, extract_non_black_rows_from_excel


@pytest.mark.parametrize("text, expected", [
    ('Name', 'name'),
    ('name', 'name'),
    ('User Name', 'user_name'),
    ('User name', 'user_name'),
    ('user name', 'user_name'),
    ('user Name', 'user_name'),
    ('user Name', 'user_name'),
    ('first middle last', 'first_middle_last'),
    ('first middle/last', 'first_middle_last'),
])
def test_to_snake_case(text, expected):
    assert to_snake_case(text) == expected


@pytest.mark.parametrize("text", [
    'dir/name_20190101_to_20221231.xlsx',
    'dir-dir/name_20190101_to_20221231.xlsx',
    'name_20190101_to_20221231.xlsx',
    'name_name1_20190101_to_20221231.xlsx',
    'name.csv'
])
def test_file_names(text):
    pattern = r'^[\w/-]+(_\d{0,8}_to_\d{8})*(.xlsx|.csv)$'
    assert re.match(pattern, text)


def test_yellow_rows():
    yellow = ['FFFF00']
    df = extract_colored_rows('yellow_rows.xlsx', yellow)

    assert len(df) == 2
    assert (df['Color'] == 'FFFF00').all()


def test_yellow_green_rows():
    df = extract_colored_rows('yellow_green_rows.xlsx', ['FFFF00', '00B050'])
    print(df)
    excepted = pd.Series(['FFFF00', '00B050', '00B050', 'FFFF00'], index=df.index)
    assert len(df) == 4
    assert (df['Color'] == excepted).all()


def test_should_return_none_when_no_rows_starting_from_the_one_containing_the_header_name_have_colored_cells():
    with open('data/no_colored_cells.xlsx', 'rb') as f:
        file_content = f.read()
    file_stream = BytesIO(file_content)
    df = extract_non_black_rows_from_excel(file_stream, 'Name')
    assert df is None


def test_should_return_the_rows_with_colored_cells_and_the_rows_starting_from_the_one_containing_the_header_name():
    with open('data/colored_cells.xlsx', 'rb') as f:
        file_content = f.read()
    file_stream = BytesIO(file_content)
    df = extract_non_black_rows_from_excel(file_stream, 'Name')
    assert len(df) == 5


def test_rename_columns():
    data = {'Column1': [1, 2, 3, 4, 5]}
    df = pd.DataFrame(data)
    excepted = pd.Series([1, 2, 3, 4, 5], index=df.index)

    column_mapping = {'Column1': 'col_1'}
    df = rename_columns(column_mapping, df)
    assert (df['col_1'] == excepted).all()


def test_csv():
    data = [
        {'Project': 'Shipment', 'Filename': 'f1', 'Last Modified': '1683767288.5960574',
         'Created At': '2023-07-26 09:17:45', 'Created By': 'System', 'Updated At': '2023-07-26 09:17:45',
         'Updated By': 'System'},
        {'Project': 'Shipment', 'Filename': 'f2', 'Last Modified': '1683767288.5960574',
         'Created At': '2023-07-26 09:17:45', 'Created By': 'System', 'Updated At': '2023-07-26 09:17:45',
         'Updated By': 'System'},
    ]
    df = pd.DataFrame(data)
    df.to_csv(work_directory + os.sep + 'history.csv', index=False)


def test_df():
    # Sample DataFrame with potential duplicates in 'Attribute'
    data = {
        'ID': [1, 1, 2, 2, 3, 4],
        'Name': ['Alice', 'Alice', 'Bob', 'Bob', 'Charlie', 'David'],
        'Attribute': ['Fast', 'Fast', 'Tall', 'Smart', 'Wise', 'Strong']
    }

    df = pd.DataFrame(data)

    # Display original DataFrame
    print("Original DataFrame:")
    print(df)

    # Remove duplicates based on 'ID' and 'Name'
    # df_unique = df.drop_duplicates(subset=['ID', 'Name'])

    # Group by 'ID' and join 'Attribute' strings, removing duplicates within groups
    id_string = ', '.join(str(x) for x in df['ID'].unique())

    # Display the result
    print(id_string)
