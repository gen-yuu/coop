import mysql.connector
from mysql.connector import Error
import os

# データベースの設定
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PW'),
    'database': os.getenv('DB_NAME')
}

abs_dirpath = os.path.dirname(os.path.abspath(__file__))  # 絶対パスを取得
sql_dir = os.path.join(abs_dirpath, 'sqls')


def exec_sql_cmd(path_to_sql, replace_dict={}):
    try:
        with mysql.connector.connect(autocommit=True, **db_config) as conn:
            with conn.cursor() as cur:
                with open(path_to_sql, 'r') as f:
                    sql = f.read()
                    for key, val in replace_dict.items():
                        sql = sql.replace(key, val)
                    cur.execute(sql)
                rows = cur.fetchall()
        return rows
    except Error as err:
        return err


def get_items(barcode_data):
    """取得したバーコードのid, name, priceを取得
    barcodeがDBに登録済み
        → id, name, price を返す
    barcodeが未登録
        → 空の配列を返す
    barcodeに登録された商品が複数
        → error
    """
    sql_path = os.path.join(sql_dir, 'get_items.sql')
    rows = exec_sql_cmd(sql_path, replace_dict={'BARCODE': str(barcode_data)})
    if len(rows) == 1:
        return rows[0]
    elif len(rows) == 0:
        return barcode_data
    else:
        print('error')


def get_user(value):
    """取得したバーコードのid, name, priceを取得
    barcodeがDBに登録済み
        → id, name, price を返す
    barcodeが未登録
        → 空の配列を返す
    barcodeに登録された商品が複数
        → error
    """
    sql_path = os.path.join(sql_dir, 'get_user.sql')
    rows = exec_sql_cmd(sql_path, replace_dict={'NFC_ID': str(value)})
    if len(rows) == 1:
        return rows[0]
    elif len(rows) == 0:
        return value
    else:
        print('error')
