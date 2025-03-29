import os
import pymysql

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PW")
DB_NAME = os.getenv("DB_NAME")


def get_connection():
    return pymysql.connect(host=DB_HOST,
                           user=DB_USER,
                           password=DB_PASSWORD,
                           db=DB_NAME,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


def get_product_by_barcode(barcode):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM items WHERE code = %s LIMIT 1"
            cursor.execute(sql, (barcode,))
            return cursor.fetchone()


def get_user_by_nfc_data(nfc_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE nfc_id = %s LIMIT 1"
            cursor.execute(sql, (nfc_id,))
            return cursor.fetchone()
