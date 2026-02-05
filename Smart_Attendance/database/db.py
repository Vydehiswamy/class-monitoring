import sqlite3
import os

# Database folder & file
DB_FOLDER = "database"
DB_NAME = "attendance.db"
DB_PATH = os.path.join(DB_FOLDER, DB_NAME)


def get_db_connection():
    """
    Creates and returns a database connection
    """
    os.makedirs(DB_FOLDER, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    """
    Creates required tables if they do not exist
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Present students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS present_students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll_no TEXT,
            section TEXT,
            branch TEXT,
            year TEXT,
            date TEXT,
            time TEXT
        )
    """)

    # Absent students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS absent_students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll_no TEXT,
            section TEXT,
            branch TEXT,
            year TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("✅ Database and tables created successfully")
