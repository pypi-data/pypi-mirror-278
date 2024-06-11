import copy
import inspect
import os
from functools import lru_cache
from typing import Any, Optional

from python_sdk_remote.utilities import get_environment_name
from python_sdk_remote.utilities import our_get_env
from url_remote.environment_name_enum import EnvironmentName

from .table_columns import table_columns
from .table_definition import table_definition
from .to_sql_interface import ToSQLInterface


def get_sql_hostname() -> str:
    return our_get_env("RDS_HOSTNAME")


def get_sql_username() -> str:
    return our_get_env("RDS_USERNAME")


def get_sql_password() -> str:
    return our_get_env("RDS_PASSWORD")


def get_sql_port() -> str:
    return our_get_env("RDS_PORT", default="3306")


def get_ssh_hostname() -> str:
    return our_get_env("SSH_HOSTNAME", raise_if_not_found=False)


def get_ssh_username() -> str:
    return our_get_env("SSH_USERNAME", raise_if_empty=True)


def get_ssh_port() -> str:
    return our_get_env("SSH_PORT", raise_if_empty=True)


def get_private_key_file_path() -> str:
    return our_get_env("PRIVATE_KEY_FILE_PATH", raise_if_empty=True)


# TODO: class DatabaseMysqlUtils(metaclass=MetaLogger, object=object_database):
def validate_select_table_name(view_table_name: str, is_ignore_duplicate: bool = False) -> None:
    # TODO: try to detect the table name from the view name (with warning)
    if (get_environment_name() not in (EnvironmentName.DVLP1.value, EnvironmentName.PROD1.value)
            and not view_table_name.endswith("_view") and not is_ignore_duplicate):
        raise Exception(
            f"View name must end with '_view' in this environment (got {view_table_name})")


def validate_none_select_table_name(table_name: str) -> None:
    if (get_environment_name() not in (EnvironmentName.DVLP1.value, EnvironmentName.PROD1.value)
            and not table_name.endswith("_table")):
        raise Exception(
            f"Table name must end with '_table' in this environment  (got {table_name})")


def process_insert_data_dict(data_dict: dict or None) -> (str, str, tuple):
    """Example:
    Input: {"name": "John", "coordinate": Point(1, 2)}
    Output: ("`name`, `coordinate`",
             "%s, Point(1, 2)",
            ("John", ))
    """
    if not data_dict:
        return '', '', {}

    columns = []
    values = []
    params = tuple()

    for key, value in data_dict.items():
        columns.append(f"`{key}`")
        if isinstance(value, ToSQLInterface):
            values.append(value.to_sql())
        else:
            values.append('%s')
            params += (value,)

    columns_str = ','.join(columns)
    values_str = ','.join(values)

    return columns_str, values_str, params


def process_upsert_data_dict(data_dict: dict or None, compare_with_or: bool,
                             where_compare: str or None = None,
                             params_compare: tuple or None = None) -> (str, tuple):
    where_clauses = []
    params = []
    for column, value in data_dict.items():
        if isinstance(value, list):
            where_clauses.append(f"({' OR '.join([f'{column}=%s' for _ in value])})")
            params.extend(value)
        elif isinstance(value, ToSQLInterface):
            where_clauses.append(f"{column}={value.to_sql()}")
        else:
            where_clauses.append(f"{column}=%s")
            params.append(value)

    where_clause = " OR " if compare_with_or else " AND "
    where_clause = where_clause.join(where_clauses)
    if where_compare and params_compare:
        if where_clause:
            where_clause = f"({where_clause}) AND ({where_compare})"
        else:
            where_clause = where_compare
        params += params_compare
    return where_clause, params


def process_update_data_dict(data_dict: dict or None) -> (str, tuple):
    """Example:
    Input: {"name": "John", "coordinate": Point(1, 2)}
    Output: ("name=%s, coordinate=Point(1, 2)", ("John", ))
    """
    if not data_dict:
        return '', {}

    set_values = []
    params = tuple()
    for key, value in data_dict.items():
        if isinstance(value, ToSQLInterface):
            set_values.append(f"`{key}`={value.to_sql()}")
        else:
            set_values.append(f"`{key}`=%s")
            params += (value,)

    # + "," because we add updated_timestamp in the update query
    set_values_str = ', '.join(set_values) + ","
    return set_values_str, params


def process_select_data_dict(data_dict: dict or None, select_with_or: bool = False) -> (str, tuple):
    """Example:
    Input: {"name": "John", "coordinate": Point(1, 2)}
    Output: ("name=%s AND coordinate=Point(1, 2)", ("John", ))
    """
    if not data_dict:
        return '', {}

    where_clauses = []
    params = tuple()
    for key, value in data_dict.items():
        if isinstance(value, list):
            where_clauses.append(f"({' OR '.join([f'{key}=%s' for _ in value])})")
            params += tuple(value)
        elif isinstance(value, ToSQLInterface):
            where_clauses.append(f"{key}={value.to_sql()}")
        else:
            where_clauses.append(f"{key}=%s")
            params += (value,)

    where_clause = " OR " if select_with_or else " AND "
    where_clause = where_clause.join(where_clauses)
    return where_clause, params


@lru_cache
def detect_if_is_test_data() -> bool:
    """Check if running from a Unit Test file."""
    possible_current_files = [os.path.basename(frame.filename) for frame in inspect.stack()]
    is_test_data = any(file_name.startswith('test_') or file_name.endswith('_test.py') or "pytest" in file_name
                       for file_name in possible_current_files)
    return is_test_data


def get_entity_type_by_table_name(table_name: str) -> int or None:
    """Returns the entity_type_id of the table."""
    entity_type_id = table_definition.get(table_name, {}).get("entity_type_id1")
    return entity_type_id


def generate_table_name(schema_name: Optional[str]) -> Optional[str]:
    if schema_name:
        return schema_name + "_table"


def generate_view_name(table_name: Optional[str]) -> Optional[str]:
    if table_name:
        view_name = table_name.replace("_table", "_view")
        return view_name
    return table_name


def generate_column_name(table_name: Optional[str]) -> Optional[str]:
    if table_name:
        column_name = table_name.replace("_table", "_id")
        return column_name


def validate_single_clause_value(select_clause_value: str = None) -> None:
    if not select_clause_value or "," in select_clause_value or select_clause_value == "*":
        raise ValueError(f"select value requires a single column name, got {select_clause_value}")


def get_where_params(column_name: str, column_value: Any) -> tuple:
    # If we use "if column_value:" it will not work for 0, False, etc.
    if not column_name:
        raise ValueError(f"column_name is required, got {column_name}")
    if isinstance(column_value, ToSQLInterface):
        where = f"`{column_name}`={column_value.to_sql()}"
        params = None
    elif column_value is not None:
        if isinstance(column_value, (list, tuple, set)):
            where = f"`{column_name}` IN (" + ",".join(["%s"] * len(column_value)) + ")"
            params = tuple(column_value)
        else:
            where = f"`{column_name}`=%s"
            params = (column_value,)
    else:
        where = f"`{column_name}` IS NULL"
        params = None
    return where, params


def where_skip_null_values(where: str or None, select_clause_value: str,
                           skip_null_values: bool = True) -> str:
    if skip_null_values:
        validate_single_clause_value(select_clause_value)
        where_skip = f"`{select_clause_value}` IS NOT NULL"
        if where:
            where += f" AND {where_skip}"
        else:
            where = where_skip
    return where


@lru_cache(maxsize=64)
def replace_view_with_table(view_table_name: str, select_clause_value: str = None) -> str:
    # test data does not appear in the view, but we still wants to access it in tests.
    if not view_table_name:
        return view_table_name
    # Guess the table name from the view name:
    table_name = remove_tag(view_table_name.replace("_view", "_table"))
    scan_table_definition_for_table_name = table_definition.get(table_name, {}).get("view_name") != view_table_name
    if scan_table_definition_for_table_name:
        for table, values in table_definition.items():
            if values["view_name"] == view_table_name:
                table_name = table  # got a better guess
                break
    if select_clause_value and select_clause_value != "*":
        requiered_columns = tuple(col.strip() for col in select_clause_value.split(","))  # if columns are specified
    else:
        requiered_columns = table_columns.get(view_table_name, [])  # all columns in the view

    # Replace 'ST_X(coordinate)' and 'ST_Y(coordinate)' with 'coordinate'
    requiered_columns = tuple('coordinate' if col in ('ST_X(coordinate)', 'ST_Y(coordinate)') else
                              remove_tag(col) for col in requiered_columns)
    if table_name in table_columns and all(  # if all requiered columns from the view present in the table.
            remove_tag(col) in table_columns.get(table_name, []) for col in requiered_columns):
        return table_name
    return view_table_name  # appropriate table not found


def remove_tag(name: str) -> str:
    return name.replace("`", "")


def insert_is_undelete(table_name: str) -> bool:
    is_undelete = table_definition.get(table_name, {}).get("insert_is_undelete")
    return is_undelete


def is_end_timestamp_in_table(table_name: str) -> bool:
    # table_definition outdated for now.
    # is_end_timestamp_in_table = table_definition.get(table_name, {}).get("end_timestamp")
    is_end_timestamp_in_table = is_column_in_table(table_name, "end_timestamp")
    return is_end_timestamp_in_table


def is_column_in_table(table_name: str, column_name: str) -> bool:
    columns = table_columns.get(table_name, [])
    return remove_tag(column_name) in columns


def get_table_columns(table_name: str = None) -> tuple:
    table_columns_tuple = table_columns.get(table_name, [])
    return table_columns_tuple


def group_list_by_columns(list_of_dicts: list, group_by: str, condense: bool = True) -> dict[tuple or str, list]:
    """if condense is True and there is only one column left in the dict, return the value instead of the dict.
    Examples:
    Input: [{"name": "John", "age": 25}, {"name": "John", "age": 26}], group_by="name"
            -> {"John": [25, 26]}
    Input: [{"name": "John", "age": 25}, {"name": "John", "age": 26}], group_by="name", condense=False
            -> {"John": [{"age": 25}, {"age": 26}]}
    Input: [{"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 4}, {"a": 2, "b": 2, "c": 5}], group_by="a"
            -> {1: [{"b": 2, "c": 3}, {"b": 2, "c": 4}], 2: [{"b": 2, "c": 5}]}
    Input: [{"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 4}, {"a": 2, "b": 2, "c": 5}], group_by="a,b", condense=False
            -> {(1, 2): [{"c": 3}, {"c": 4}], (2, 2): [{"c": 5}]}
    """
    group_by = tuple(map(str.strip, group_by.split(",")))
    if not list_of_dicts:
        return {}
    list_of_dicts = copy.deepcopy(list_of_dicts)
    if any(col not in list_of_dicts[0] for col in group_by):
        raise ValueError(f"{group_by} should be a subset of {tuple(list_of_dicts[0].keys())}")
    if len(group_by) == len(list_of_dicts[0]):
        raise ValueError(f"Column names in group_by must be less than the number of columns in the list of dicts")
    grouped = {}
    for dict_row in list_of_dicts:
        key = tuple(dict_row[col] for col in group_by) if len(group_by) > 1 else dict_row[group_by[0]]
        if key not in grouped:
            grouped[key] = []
        for col in group_by:
            dict_row.pop(col)
        grouped[key].append(dict_row if not condense or len(dict_row) > 1 else next(iter(dict_row.values())))
    return grouped


# Not used anymore:
# def extract_duplicated_from_error(error: Exception) -> (Any, str):
# """Error examples:
# - Duplicate entry '1' for key 'test_mysql_table.PRIMARY'  - in such case return the duplicated value, otherwise the column
# - Duplicate entry '7263200721327371865' for key 'test_mysql_table.number_UNIQUE
# - IntegrityError(1062, "1062 (23000): Duplicate entry '202-405-3018' for key 'person_table.person.main_full_number_normalized_UNIQUE'", '23000')
# - Duplicate entry 'test@gmail.com' for key 'email_address_table.email_address.unique'
# - 1062 (23000): Duplicate entry 'tal@circlez.ai' for key 'person_table.person_table.main_email_person.unique'
# - TODO (index can have any name): 1062 (23000): Duplicate entry '1-2' for key 'test_location_profile_table.idx_location_id_profile_id'
# """
# pattern = r'Duplicate entry \'(.+?)\' for key \'(.+?)\''
# match = re.search(pattern, str(error))
# if not match:  # a different error
#     raise error
# duplicate_value = match.group(1)
# key = match.group(2)
# if key.endswith("PRIMARY"):
#     return int(duplicate_value), ""
# elif key.endswith("_UNIQUE"):
#     # all but last
#     duplicate_column_name = "_".join(key.split(".")[-1].split('_')[:-1])
# elif key.count(".") > 1:
#     duplicate_column_name = key.split(".")[-2]
# else:
#     raise Exception(f"GenericCRUD._get_existing_duplicate_id: please report the following error,"
#                     f" so we can add support to this case: insert error: {error}")
# return duplicate_value, duplicate_column_name

def generate_where_clause_for_ignore_duplicate(data_dict: dict, constraint_columns: list[list[str]]) -> (str, tuple):
    where_clauses = []
    values = []

    for constraint_column in constraint_columns:
        # Handle special case for 'point' or 'coordinate'
        formatted_columns = []
        temp_values = []

        for column in constraint_column:
            if column in data_dict:
                if column == 'point' or column == 'coordinate':
                    formatted_columns.append('ST_X(coordinate) = %s')
                    temp_values.append(data_dict[column])
                    formatted_columns.append('ST_Y(coordinate) = %s')
                    temp_values.append(data_dict[column])
                else:
                    formatted_columns.append(f"{column} = %s")
                    temp_values.append(data_dict[column])

        if (len(temp_values) == len(constraint_column) *
                (2 if 'point' in constraint_column or 'coordinate' in constraint_column else 1)):
            where_clauses.append(f"({' AND '.join(formatted_columns)})")
            values.extend(temp_values)

    if where_clauses:
        where = ' OR '.join(where_clauses)
        return where, tuple(values)
    return "", tuple()

# TODO: run this with cache decorator if the above get_table_columns doesn't find anything.
# def get_table_columns(schema_name: str = None, table_name: str = None) -> tuple:
#     select_query = "SELECT column_name " \
#                    "FROM information_schema.columns " \
#                    "WHERE TABLE_SCHEMA = %s " \
#                    "AND TABLE_NAME = %s;"
#     params = (schema_name, table_name)
#
#     self.connection.commit()
#     self.cursor.execute(select_query, params)
#     result = self.cursor.fetchall()
#
#     columns_tuple = tuple(x[0] for x in result)
#     self.logger.debug(object=locals())
#     return columns_tuple
