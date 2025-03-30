import eventlet
# Pythonの標準ライブラリを非同期I/Oに対応するように書き換えます。
eventlet.monkey_patch()
from eventlet import wsgi
import pika
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import json
from db_api.database import *
from utils.formatters import build_item_info, build_user_info

app = Flask(__name__)
CORS(app)  # ReactとFlaskが別サーバーならCORSを有効化
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')  # WebSocketを有効化

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PW = os.getenv("RABBITMQ_PW")

# -------------------- RabbitMQのメッセージ処理 --------------------


def on_rabbitmq_message_item(body):
    """
    RabbitMQからのメッセージ（バーコード）を受信し、DBから商品情報を取得してWebSocketで送信
    """
    barcode = body.decode()
    print(f"Received barcode from RabbitMQ: {barcode}")

    # # DBから商品情報を取得
    try:
        item_data = get_product_by_barcode(barcode)
    except Exception as e:
        print(f"DBエラー: {e}")
        item_data = None

    # WebSocketを通じてフロントエンドに商品情報を送信
    if item_data:
        item_info = build_item_info(item_data)
        print(f"Sending product data: {item_info}")

        # WebSocketを通じてフロントエンドに商品情報を送信
        socketio.emit("item_registered", item_info)
    else:
        print(f"No product found for barcode: {barcode}")
        socketio.emit("item_not_found", {"code": barcode})
    return 0


def on_rabbitmq_message_user(body):
    """
    RabbitMQからのNFCメッセージを受信し、DBからユーザー情報を取得してWebSocketで送信
    """
    nfc_data = body.decode()
    print(f"Received NFC data from RabbitMQ: {nfc_data}")

    # DBからユーザー情報を取得
    # # DBから商品情報を取得
    try:
        user_data = get_user_by_nfc_data(nfc_data)
    except Exception as e:
        print(f"DBエラー: {e}")
        user_data = None

    if user_data:
        user_info = build_user_info(user_data)
        print(f"Sending user data: {user_info}")

        # WebSocketを通じてフロントエンドにユーザー情報を送信
        socketio.emit("user_registered", user_info)
    else:
        print(f"No user found for NFC data: {nfc_data}")
        socketio.emit("user_not_found", {"nfc_id": nfc_data})
    return 0


# Define a function to set up RabbitMQ connection and channel
def setup_rabbitmq():
    """
    RabbitMQの接続を設定
    """
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PW)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='barcode_queue')
    channel.queue_declare(queue='nfc_queue')

    # Set up consumers
    channel.basic_consume(
        queue='barcode_queue',
        on_message_callback=lambda ch, method, properties, body: on_rabbitmq_message_item(body),
        auto_ack=True)
    channel.basic_consume(
        queue='nfc_queue',
        on_message_callback=lambda ch, method, properties, body: on_rabbitmq_message_user(body),
        auto_ack=True)
    return channel


# Create a separate thread for the RabbitMQ consumer
def rabbitmq_consumer_thread():
    """
    RabbitMQのコンシューマを別スレッドで実行
    """
    channel = setup_rabbitmq()
    channel.start_consuming()


def create_app():
    """
    Flaskアプリのセットアップ
    """
    # 非同期でRabbitMQコンシューマを実行
    eventlet.spawn(rabbitmq_consumer_thread)
    return app


# -------------------- アプリ起動 --------------------
if __name__ == "__main__":
    create_app()
    wsgi.server(eventlet.listen(('0.0.0.0', 8000)), app)
