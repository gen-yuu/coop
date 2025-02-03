from flask import Flask, render_template, request
from flask_socketio import SocketIO
import pika
import eventlet
import json
import os
from utils.connect_db import *

# Pythonの標準ライブラリを非同期I/Oに対応
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# -------------------- RabbitMQ メッセージ処理 --------------------

def on_rabbitmq_message_item(body):
    """ 商品データをWebSocket経由で送信 """
    data = json.loads(body)
    socketio.emit('item_added', {
        'item_id': data[0], 'itemName': data[1], 'itemPrice': data[2],
        'stockNum': data[3], 'itemClass': data[4], 'Barcode': data[5]
    })

def on_rabbitmq_message_user(body):
    """ ユーザーデータをWebSocket経由で送信 """
    data = json.loads(body)
    socketio.emit('user_info', {
        'user_id': data[0], 'userName': data[1], 'nfc_id': data[2],
        'grade': data[3], 'balance': data[4]
    })

def on_rabbitmq_message_user_registration(body):
    """ NFC登録データをWebSocket経由で送信 """
    socketio.emit('user_nfc', {'nfc_id': body})

def on_rabbitmq_message_item_registration(body):
    """ バーコード登録データをWebSocket経由で送信 """
    socketio.emit('item_barcode', {'barcode': body.decode()})

def setup_rabbitmq():
    """ RabbitMQの接続とキューの設定 """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    queues = {
        'barcode_queue': on_rabbitmq_message_item,
        'nfc_queue': on_rabbitmq_message_user,
        'barcode_registration': on_rabbitmq_message_item_registration,
        'nfc_registration': on_rabbitmq_message_user_registration
    }

    for queue, callback in queues.items():
        channel.queue_declare(queue=queue)
        channel.basic_consume(queue=queue, on_message_callback=lambda ch, method, properties, body: callback(body), auto_ack=True)

    return channel

def rabbitmq_consumer_thread():
    """ RabbitMQのメッセージ処理を別スレッドで実行 """
    channel = setup_rabbitmq()
    channel.start_consuming()

# -------------------- WebSocketイベント --------------------

@socketio.on('confirm_purchase')
def confirm_purchase(data):
    """ 購入処理を実行し、完了通知を送信 """
    data = dict(data)
    insert_order(data)
    update_balance(data)
    socketio.emit('purchase_confirmed', {'flag': 'ok'})

# -------------------- ルーティング --------------------

@app.route('/')
def index():
    return render_template('index.html', title='Coop Shopping')

@app.route('/item_list')
def item_list():
    """ 商品一覧ページ """
    sql_path = os.path.join(sql_dir, 'get_all_items.sql')
    rows = exec_sql_cmd(sql_path)
    return render_template('item_list.html', title='商品一覧', data=rows)

@app.route('/product_registration', methods=["GET", "POST"])
def product_registration():
    """ 商品登録ページ """
    if request.method == "POST":
        data = dict(request.form)
        result = new_items_or_update_items(data)
        message = '商品登録ができました' if isinstance(result, list) else result
        return render_template('product_registration.html', title='新規商品登録', message=message)

    return render_template('product_registration.html', title='新規商品登録', message='')

@app.route('/user_registration', methods=["GET", "POST"])
def user_registration():
    """ ユーザー登録ページ """
    if request.method == "POST":
        data = dict(request.form)
        if not data.get('nfcId') or not data.get('userName'):
            return render_template('user_registration.html', title='新規ユーザー登録', message='正しく入力してください')
        
        result = new_user_or_update_user(data)
        message = 'ユーザ登録ができました' if isinstance(result, list) else result
        return render_template('user_registration.html', title='新規ユーザー登録', message=message)

    return render_template('user_registration.html', title='新規ユーザー登録', message='')

# -------------------- アプリケーション起動 --------------------

def create_app():
    """ アプリケーションを作成し、RabbitMQのスレッドを開始 """
    eventlet.spawn(rabbitmq_consumer_thread)
    return app

if __name__ == '__main__':
    create_app()
    eventlet.wsgi.server(eventlet.listen(("192.168.2.198", 8080)), app)