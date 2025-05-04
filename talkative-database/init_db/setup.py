import sqlite3


def create_tables():
    with open("create.sql", "r") as file:
        sql_script = file.read()

    conn = sqlite3.connect("myDataBase.db")

    cursor = conn.cursor()
    cursor.executescript(sql_script)

    print("Tables created successfully.")


if __name__ == "__main__":
    create_tables()
