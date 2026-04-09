import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="crossover.proxy.rlwy.net",
            port="46708",
            user="root",
            password="PduGufscOXTvYlQvSmvwXtcSzYmLxiaO",
            database="railway"
        )
        return conn
    except Error as e:
        print(f"MySQL connection error: {e}")
        return None

def get_cursor():
    conn = get_connection()
    if conn:
        return conn, conn.cursor()
    return None, None