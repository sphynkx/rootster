import hashlib
import datetime
from config import MYSQL_CONFIG
from db import get_db


def check_admin(username, password):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM admins WHERE username=%s AND is_active=1", (username,))
            admin = cursor.fetchone()
            if admin:
                pwd_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
                if admin["password_hash"] == pwd_hash:
                    cursor.execute(
                        "UPDATE admins SET last_login = %s WHERE username = %s",
                        (datetime.datetime.now(), username)
                    )
                    conn.commit()
                    return True
    finally:
        conn.close()
    return False


def get_table_list():
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            return [row[f"Tables_in_{MYSQL_CONFIG['database']}"] for row in cursor.fetchall()]
    finally:
        conn.close()


def get_table_rows_and_columns(table):
    """
    Get last 100 records and columns list for table.
    """
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `{table}`  ORDER BY id DESC LIMIT 100")
            rows = cursor.fetchall()
            cursor.execute(f"SHOW COLUMNS FROM `{table}`")
            columns = [col["Field"] for col in cursor.fetchall()]
        return rows, columns
    finally:
        conn.close()
