import os
import pymysql
import datetime

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


def get_item_by_barcode(barcode):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM items WHERE code = %s LIMIT 1"
            cursor.execute(sql, (barcode,))
            return cursor.fetchone()


def get_item_by_id(id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM items WHERE id = %s LIMIT 1"
            cursor.execute(sql, (id,))
            return cursor.fetchone()


def get_user_by_nfc_data(nfc_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE nfc_id = %s LIMIT 1"
            cursor.execute(sql, (nfc_id,))
            return cursor.fetchone()


def get_user_by_id(id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE id = %s LIMIT 1"
            cursor.execute(sql, (id,))
            return cursor.fetchone()


def update_stock(item_id: int, diff: int, conn):
    """
    商品の在庫を更新する（増減）
    :param item_code: 商品コード
    :param diff: 増減数（正:加算、負:減算）
    :param conn: トランザクション中のコネクション
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE items SET stock_num = stock_num + %s WHERE id = %s",
                           (diff, item_id))


def update_balance(user_id: int, diff: int, conn):
    """
    ユーザーの残高を更新する（増減）
    :param user_id: ユーザーID
    :param diff: 増減額（正:加算、負:減算）
    :param conn: トランザクション中のコネクション
    """
    with conn.cursor() as cursor:
        cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (diff, user_id))


def insert_order(user_id: int, conn) -> int:
    now = datetime.datetime.now()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO orders (user_id, datetime) VALUES (%s, %s)", (user_id, now))
        order_id = cursor.lastrowid  # ← 自動採番された注文IDを取得
    return order_id


def insert_order_item(order_id: int, item: dict, quantity: int, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO order_items (order_id, item_id, item_name, item_price, item_class, quantity) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (order_id, item["id"], item["name"], item["price"], item["class"], quantity))
