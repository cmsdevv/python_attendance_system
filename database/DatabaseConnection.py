import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="attendance_system"
        )
        return conn
    except Exception as e:
        print(f"CONNECTION ERROR: {e}")
        return None