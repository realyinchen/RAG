from langchain_community.utilities import SQLDatabase


def get_database_config():
    # SQLite
    try:
        sqlite_db = SQLDatabase.from_uri("sqlite:///init_db/myDataBase.db")
        sqlite_info = sqlite_db.get_table_info()
    except Exception as e:
        sqlite_db = None
        sqlite_info = f"Error retrieving table info: {str(e)}"

    return {
        "db": sqlite_db,
        "description": "Northwind retail dataset (e.g. customers, products, orders)",
        "table_info": sqlite_info,
    }
