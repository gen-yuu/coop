from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from app.services.database import save_nfc_data, save_barcode_data
import os
import eventlet
from eventlet import wsgi
import pika
import json
from api.database import *

API_PORT = int(os.environ.get("API_PORT"))
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


def create_app():
    eventlet.spawn(rabbitmq_consumer_thread)
    return app


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
