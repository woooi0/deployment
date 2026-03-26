import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="crossover.proxy.rlwy.net",
            port="46708",
            user="root",
            password="PduGufscOXTvYlQvSmvwXtcSzYmLxiaO",
            database="railway"
        )
        yield conn
    except Error as e:
        print(f"MySQL connection error: {e}")
        yield None
    finally:
        if conn and conn.is_connected():
            conn.close()
