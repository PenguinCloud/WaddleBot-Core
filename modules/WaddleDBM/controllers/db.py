# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from db.py")

# This controller is responsible for creating DB tables, querying the DB, and inserting data into the DB.

# Function to insert a given table_name and columns into a configuration file.
def insert_table_into_config(table_name, columns):
    # Check if the table_name and columns are given.
    if not table_name or not columns:
        return dict(msg="Please provide a table_name and columns.")

    filePath = "applications/WaddleDBM/models/external_tables.json"
    tableList = []

    # Check if the configuration file exists.
    try:
        with open(filePath, "r") as file:
            tableList = json.load(file)

    except FileNotFoundError:
        print("Configuration file not found. Creating a new configuration file.")
    
    # Check if the table_name already exists in the configuration file.
    if len(tableList) > 0:
        for table in tableList:
            if "table_name" in table and table["table_name"] == table_name:
                return dict(msg=f"Table {table_name} already exists in the configuration file.")
    
    # Insert the table_name and columns into the configuration file.
    config = {
        "table_name": table_name,
        "columns": columns
    }

    tableList.append(config)
    
    # Write the updated configuration file.
    with open(filePath, "w") as file:
        json.dump(tableList, file)
    
    return dict(msg=f"Table {table_name} inserted into the configuration file.")

# Function to get all tables from the configuration file, and define them in the pydal database.
def define_tables_from_config():
    print("Defining tables from the configuration file.")

    filePath = "applications/WaddleDBM/models/external_tables.json"
    tableList = []

    # Check if the configuration file exists.
    try:
        with open(filePath, "r") as file:
            tableList = json.load(file)

    except FileNotFoundError:
        return dict(msg="Configuration file not found.")
    
    # Check if the tableList is empty.
    if not tableList:
        return dict(msg="No tables found in the configuration file.")
    
    # Define all the tables in the configuration file.
    if len(tableList) > 0:
        print("Found tables in the configuration file. Defining tables in the database.")
        for table in tableList:
            table_name = table.get("table_name")
            columns = table.get("columns")
            
            # Check if the table_name and columns are given.
            if not table_name or not columns:
                return dict(msg="Please provide a table_name and columns.")
            
            # Check if the table already exists.
            if db.get(table_name):
                return dict(msg=f"Table {table_name} already exists.")
            
            # The columns is read as a dictionary with the column name as the key and the column type as the value.
            # Convert the dictionary into 2 lists, one for the column names and one for the column types.
            tColumns = list(columns.keys())
            tTypes = list(columns.values())
            
            try:
                # Create the table with the given columns.
                db.define_table(table_name, *[Field(column_name, column_type) for column_name, column_type in zip(tColumns, tTypes)])

                # Commit the table creation.
                db.commit()

                print(f"Table {table_name} defined with columns {tColumns}.")
            except Exception as e:
                return dict(msg=f"Error creating table {table_name}. Error: {e}")
    
    # Print all the tables defined from the configuration file.
    print(db.tables())

    return dict(msg="All tables defined from the configuration file.")

# Function to use a payload to create a new pydal table.
def initialize():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given. Please provide a table_name and fields between [] characters.")
    payload = json.loads(payload)
    
    # Check if the table_name and column fields are given in the payload.
    if "table_name" not in payload or "columns" not in payload:
        return dict(msg="Please provide a table_name and columns payload values.")
    
    table_name = payload.get("table_name")
    columns = payload.get("columns")

    # The columns is read as a dictionary with the column name as the key and the column type as the value.
    # Convert the dictionary into 2 lists, one for the column names and one for the column types.
    tColumns = list(columns.keys())
    tTypes = list(columns.values())
    
    # Check if the table already exists.
    if db.get(table_name):
        return dict(msg=f"Table {table_name} already exists.")
    
    try:
        # Create the table with the given columns.
        db.define_table(table_name, *[
            Field(column_name, column_type) for column_name, column_type in zip(tColumns, tTypes)
        ])

        # Commit the table creation.
        db.commit()

        # Insert the table into the configuration file.
        msg = insert_table_into_config(table_name, columns)

        print(msg)

    except Exception as e:
        return dict(msg=f"Error creating table {table_name}. Error: {e}")
    
    return dict(msg=f"Table {table_name} created with columns {tColumns}.")

# Function to use a payload to read data from a pydal table.
def read():
    define_tables_from_config()

    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given. Please provide a table_name and query between [] characters.")
    payload = json.loads(payload)
    
    # Check if the table, column, matchColumn, and matchValue are given in the payload.
    if "table" not in payload or "column" not in payload or "matchColumn" not in payload or "matchValue" not in payload:
        return dict(msg="Please provide a table, column, matchColumn, and matchValue payload values.")
    
    table = payload.get("table")
    column = payload.get("column")
    matchColumn = payload.get("matchColumn")
    matchValue = payload.get("matchValue")

    # Check that the column value is not empty and a string.
    if not column or not isinstance(column, str):
        return dict(msg='The "column" value should not be empty and should be a string.')

    # Check if the table exists.
    if not db.get(table):
        return dict(msg=f"Table {table} does not exist.")
    
    # Get the table object.
    table = db[table]
    
    try:
        # Query the table for the record.
        record = db(table[matchColumn] == matchValue).select().first()

        # If the column value is "*", return all columns.
        if column == "*":
            outVal = record.as_dict()
        # Else split the column value by "," and the values of the columns in the record.
        else:
            columns = column.split(",")
            outVal = {col: record[col] for col in columns}
    except Exception as e:
        return dict(msg=f"Error querying table {table}. Error: {e}")
    
    return dict(data=outVal)

# Function to use a payload to insert data into a pydal table.
def insert():
    define_tables_from_config()

    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given. Please provide a table_name and data between [] characters.")
    payload = json.loads(payload)
    
    # Check if the table_name and data are given in the payload.
    if "table_name" not in payload or "data" not in payload:
        return dict(msg="Please provide a table_name and data payload values.")
    
    table_name = payload.get("table_name")
    data = payload.get("data")
    
    # Get all the tables in the database.
    tables = db.tables()

    # Check if the table exists.
    if not db.get(table_name):
        return dict(msg=f"Table {table_name} does not exist.")
    
    # Check if the data is a list of dictionaries.
    if not isinstance(data, list):
        return dict(msg="Data should be a list of dictionaries.")
    
    # Check if the data is not empty.
    if not data:
        return dict(msg="Data should not be empty.")
    
    # Get the table object.
    table = db[table_name]
    
    try:
        # Insert the data into the table.
        table.bulk_insert(data)
    except Exception as e:
        return dict(msg=f"Error inserting data into table {table_name}. Error: {e}")
    
    return dict(msg=f"Data inserted into table {table_name}.")

# Function to use a payload to update data in a pydal table. If the record does not exist, insert the data.
def update():
    define_tables_from_config()

    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given. Please provide a table_name and data between [] characters.")
    payload = json.loads(payload)
    
    # Check if the table, column, matchColumn, matchValue, updateValue are given in the payload.
    if "table" not in payload or "column" not in payload or "matchColumn" not in payload or "matchValue" not in payload or "updateValue" not in payload:
        return dict(msg="Please provide a table_name, column, matchColumn, matchValue, and updateValue payload values.")
    
    table = payload.get("table")
    column = payload.get("column")
    matchColumn = payload.get("matchColumn")
    matchValue = payload.get("matchValue")
    updateValue = payload.get("updateValue")

    # Check if the table exists.
    if not db.get(table):
        return dict(msg=f"Table {table} does not exist.")
    
    # Get the table object.
    table = db[table]
    
    try:
        # Update the record in the table.
        record = db(table[matchColumn] == matchValue).select().first()
        if record:
            record.update_record(**{column: updateValue})

    except Exception as e:
        return dict(msg=f"Error updating data in table {table}. Error: {e}")
    
    return dict(msg=f"Data updated in table {table}.")

