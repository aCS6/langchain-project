import sqlite3

from langchain.tools import Tool

from schemas.schema import RunQueryArgsSchema, DescribeTablesArgsSchema

# Database Connection
conn = sqlite3.connect("db.sqlite")


def list_tables():
    """Function to get the tables in sqlite databse."""
    cursor = conn.cursor()
    qry = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor.execute(qry)
    rows = cursor.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)


def run_sqlite_query(query):
    """Function to execute the sql query"""
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occured: {str(err)}"


def describe_tables(table_names):
    """Get the DB table schema"""
    print("Desctibe tables called...")
    cursor = conn.cursor()
    tables = ", ".join("'" + table + "'" for table in table_names)
    qry = f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables});"
    rows = cursor.execute(qry)
    response = "\n".join(row[0] for row in rows if row[0] is not None)
    print(response)
    return response


# tool - run_sqlite_query
run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query.",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema,
)

# tool - describe_tables
describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns the schema of those tables",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema,
)
