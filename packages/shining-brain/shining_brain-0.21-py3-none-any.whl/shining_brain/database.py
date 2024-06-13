class ColumnDefinition:
    def __init__(self, datatype: str = 'varchar', length: int = 200, default_value=None, is_null: bool = True):
        self.__datatype = datatype
        self.__length = length
        self.__default_value = default_value
        self.__is_null = is_null

    def get(self):
        default_value = "" if self.__default_value is None else f' default "{self.__default_value}"'
        return f'{self.__datatype}({self.__length}) {"null" if self.__is_null is True else "not null"}{default_value}'


class CreateDefinition:

    def __init__(self, column_name: str, column_definition: ColumnDefinition, is_last: bool = False):
        self.__column_name = column_name
        self.__column_definition = column_definition
        self.__is_last = is_last

    def get_name(self) -> str:
        return self.__column_name

    def is_last(self) -> bool:
        return self.__is_last

    def get(self):
        return f'`{self.__column_name}` {self.__column_definition.get()}'


class CreateTableStatement:
    def __init__(self, table_name: str, create_definitions: list):
        self.__table_name = table_name
        self.__create_definitions = create_definitions

    def get(self) -> str:
        statement = [f'drop table if exists {self.__table_name};\n', f'create table {self.__table_name} (\n\t']

        create_definitions = []
        for create_definition in self.__create_definitions:
            create_definitions.append(create_definition.get())

        if len(create_definitions) > 1:
            statement.append(',\n\t'.join(create_definitions))
        if len(create_definitions) == 1:
            statement.append(create_definitions.pop())

        statement.append('\n' + ')')
        return ''.join(statement)


class CreateIndexStatement:
    def __init__(self, table_name, column_name):
        self.__table_name = table_name
        self.__column_name = column_name

    def get(self) -> str:
        return f'create index {self.__column_name}_index on {self.__table_name} ({self.__column_name})'
