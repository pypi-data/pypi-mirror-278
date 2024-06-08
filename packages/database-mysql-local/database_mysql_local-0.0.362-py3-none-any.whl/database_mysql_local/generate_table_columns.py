import json

from database_mysql_local.connector import Connector

# TODO improve Sql2Code. We prefer only Sql2Code to generate those structures.

connection = Connector.connect(schema_name="test")
try:
    tables_and_columns = {}
    cursor = connection.cursor()
    query = """SELECT TABLE_NAME, COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA <> 'information_schema'"""

    # Execute the query
    cursor.execute(query)
    result = cursor.fetchall()

    # Process the results and group by table name
    for row in result:
        table_name, column_name = row
        if table_name not in tables_and_columns:
            tables_and_columns[table_name] = []
        tables_and_columns[table_name].append(column_name)
    table_columns_json = json.dumps(tables_and_columns, indent=4).replace("[", "(").replace("]", ")")
    with open("table_columns.py", "w") as f:
        f.write(f"table_columns = {table_columns_json}")
finally:
    connection.close()