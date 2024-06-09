import sqlite3
import os

def connect_database(name, directory=None):
    """
    Connects to a SQLite database with the given name.
    
    Parameters:
    name (str): The name of the database.
    directory (str, optional): The directory where the database file will be created. 
                                If not provided, the directory of the script is used.
    """
    global conn
    global c

    if directory is None:
        directory = os.path.dirname(os.path.abspath(__file__))
    
    db_path = os.path.join(directory, f'{name}.db')
    print(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()  
    c.execute('SELECT SQLITE_VERSION()')
    version = c.fetchone()
    print(f'Connected to database {db_path}, version is {version[0]}')




    
    
def disconnect_database():  
    """
    Closes the connection to the SQLite database.
    """

    conn.close()
    print(f'Successfully disconnected')
    
        
def delete_database(name, directory=None):
    """
    Deletes the SQLite database file with the given name.
    
    Parameters:
    name (str): The name of the database to delete.
    directory (str, optional): The directory where the database file is located. 
                                If not provided, the directory of the script is used.
    """

    if directory is None:
        directory = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(directory, f'{name}.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f'Successfully deleted {name}.db')
    else:
        print(f'{name}.db does not exist')



def create_table(table_name, columns=None):
    """
    Create a new table with the given table_name and columns.
    If columns is not provided, it will create an empty table.
    """

    query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
    c.execute(query)
    print(f'Table {table_name} created successfully')


def drop_table(table_name):
    """
    Drop the specified table from the database.
    """

    query = f"DROP TABLE IF EXISTS {table_name}"
    c.execute(query)
    print(f'Table {table_name} dropped successfully')


def delete_row(table_name, where_clause):
    """
    Delete a row from the specified table based on the where_clause.
    """
    query = f"DELETE FROM {table_name} WHERE {where_clause}"
    c.execute(query)


def update_row(table_name, set_clause, where_clause):
    """
    Update rows in the specified table based on the set_clause and where_clause.
    """
    query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
    c.execute(query)


def select_rows(table_name, where_clause="", columns="*"):
    """
    Select rows from the specified table based on the where_clause and columns.
    """
    query = f"SELECT {columns} FROM {table_name} {where_clause}"
    c.execute(query)
    return c.fetchall()



def insert_row(table_name, values):
    """
    Insert a new row into the specified table with the given values.
    Automatically skips the 'id' column if it's defined as INTEGER PRIMARY KEY.
    
    Parameters:
    table_name (str): The name of the table.
    values (list): The values to insert into the table.
    """
    # Get the table info to determine the columns
    c.execute(f"PRAGMA table_info({table_name})")
    columns_info = c.fetchall()
    
    # Extract column names, skipping the 'id' column
    columns = [col[1] for col in columns_info if col[1] != 'id']
    
    # Construct the INSERT query
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in values])})"
    c.execute(query, values)
    conn.commit()


def execute_query(query):
    """
    Execute a query with the given query string.
    """
    c.execute(query)


def print_table(table_name):
    """
    Prints the columns and contents of the specified table.
    
    Parameters:
    table_name (str): The name of the table.
    """

    c.execute("SELECT * FROM {}".format(table_name))
    rows = c.fetchall()

    if not rows:
        print("Table '{}' is empty.".format(table_name))
        return

    column_names = [description[0] for description in c.description]
    column_widths = [max(len(str(value)) for value in column) for column in zip(*rows, column_names)]
    format_str = ' | '.join('{{:<{}}}'.format(width) for width in column_widths)
    header = format_str.format(*column_names)
    print(header)
    print('-' * len(header))

    for row in rows:
        print(format_str.format(*row))


"""
#Tests
database_name = "test_database"
table_name = "users"
values = [["John Doe", "john@example.com", "2021-09-15"],["Jane Doe", "jane@example.com", "2021-10-12"],
              ["Bob Smith", "bob@example.com", "2021-11-01"]]

connect_database(database_name)
create_table(table_name,["id INTEGER PRIMARY KEY","name TEXT","email TEXT", "creation_date TEXT"])
for value in values:
    insert_row(table_name, value)
print_table(table_name)
print(select_rows(table_name, "WHERE id=1"))
update_row(table_name, "name='John Doe Updated'", "id=1")
delete_row(table_name, "id=2")
insert_row(table_name, ["John Richard", "john@example.com", "2021-09-15"])
print_table(table_name)
disconnect_database()
delete_database(database_name)
"""