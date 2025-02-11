from flask import Flask, render_template, request
from flask_socketio import SocketIO
import os
import eventlet
from eventlet import wsgi
import pika
import json
from db_api.database import *

APP_PORT = int(os.environ.get("APP_PORT"))
# 環境変数から RabbitMQ の接続情報を取得
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")

# Pythonの標準ライブラリを非同期I/Oに対応するように書き換えます。
eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')


# --------------------Connect to BARCODE and NFCREAD through RabbitMQ-----------------------------------
# Create a function to handle incoming RabbitMQ messages
def on_rabbitmq_message_item(body):
    # When a message is received, broadcast it to all connected WebSocket clients
    data = body.decode()
    item_info = get_items(data)
    if isinstance(item_info, str):
        socketio.emit('item_barcode', {'barcode': item_info})
    else:
        item_info = json.loads(item_info)
        # JSON形式に変換可能なオブジェクトである場合
        socketio.emit(
            'item_info', {
                'item_id': item_info[0],
                'itemName': item_info[1],
                'itemPrice': item_info[2],
                'stockNum': item_info[3],
                'itemClass': item_info[4],
                'Barcode': item_info[5]
            })


# Create a function to handle incoming RabbitMQ messages
def on_rabbitmq_message_user(body):
    # When a message is received, broadcast it to all connected WebSocket clients
    data = body.decode()
    user_info = get_user(data)
    if isinstance(user_info, str):
        socketio.emit('user_nfc', {'nfc_id': user_info})
    else:
        # JSON形式に変換可能なオブジェクトである場合
        user_info = json.loads(user_info)
        socketio.emit(
            'user_info', {
                'user_id': user_info[0],
                'userName': user_info[1],
                'nfc_id': user_info[2],
                'grade': user_info[3],
                'balance': user_info[4]
            })


# Define a function to set up RabbitMQ connection and channel
def setup_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='barcode_queue')
    channel.queue_declare(queue='nfc_queue')
    # channel.queue_declare(queue='barcode_registration')
    # channel.queue_declare(queue='nfc_registration')

    # Set up consumers
    channel.basic_consume(
        queue='barcode_queue',
        on_message_callback=lambda ch, method, properties, body: on_rabbitmq_message_item(body),
        auto_ack=True)
    channel.basic_consume(
        queue='nfc_queue',
        on_message_callback=lambda ch, method, properties, body: on_rabbitmq_message_user(body),
        auto_ack=True)
    # channel.basic_consume(queue='barcode_registration',
    #                       on_message_callback=lambda ch, method, properties, body:
    #                       on_rabbitmq_message_item_registration(body),
    #                       auto_ack=True)
    # channel.basic_consume(queue='nfc_registration',
    #                       on_message_callback=lambda ch, method, properties, body:
    #                       on_rabbitmq_message_user_registration(body),
    #                       auto_ack=True)
    return channel


# Create a separate thread for the RabbitMQ consumer
def rabbitmq_consumer_thread():
    channel = setup_rabbitmq()
    channel.start_consuming()


# --------------------Purchase items -------------------------------------------------------------------
# 購入処理が終わったらブラウザ側に購入処理が終わったことを通知する
@socketio.on('confirm_purchase')
def confirm_purchase(data):
    print('Received data:', data)
    data = dict(data)
    insert_order(data)
    update_balance(data)
    socketio.emit('purchase_confirmed', {'flag': 'ok'})


# --------------------Pages--------------------------------------------------------------------------------


@app.route('/')
def index():
    return render_template('index.html', title='Coop Shopping')


@app.route('/item_list')
def item_list():
    sql_path = os.path.join(sql_dir, 'get_all_items.sql')
    rows = exec_sql_cmd(sql_path)
    return render_template('item_list.html', title='商品一覧', data=rows)


@app.route('/product_registration', methods=["GET", "POST"])
def product_registration():
    if request.method == "GET":
        return render_template('product_registration.html', title='新規商品登録', message='')
    else:
        data = dict(request.form)
        result = new_items_or_update_items(data)
        if isinstance(result, list):
            return render_template('product_registration.html',
                                   title='新規商品登録',
                                   message='商品登録ができました')
        else:
            # エラー
            return render_template('product_registration.html', title='新規商品登録', message=result)


@app.route('/user_registration', methods=["GET", "POST"])
def user_registration():
    print(request.method)
    if request.method == "GET":
        return render_template('user_registration.html', title='新規ユーザー登録', message='')
    else:
        data = dict(request.form)
        if data['nfcId'] == '' or data['userName'] == '':
            return render_template('user_registration.html',
                                   title='新規ユーザー登録',
                                   message='正しく入力してください')
        result = new_user_or_update_user(data)
        if isinstance(result, list):
            return render_template('user_registration.html',
                                   title='新規ユーザー登録',
                                   message='ユーザ登録ができました')
        else:
            # エラー
            return render_template('user_registration.html', title='新規ユーザー登録', message=result)


def create_app():
    eventlet.spawn(rabbitmq_consumer_thread)
    return app


if __name__ == '__main__':
    create_app()
    wsgi.server(eventlet.listen(("0.0.0.0", 8080)), app)
