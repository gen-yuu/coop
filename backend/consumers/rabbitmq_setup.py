import pika
import os
from consumers.rabbitmq_handler import RabbitMQHandler

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PW = os.getenv("RABBITMQ_PW")


def setup_rabbitmq_consumer(socketio):
    """
    RabbitMQのチャネル設定とconsumer登録を行う
    """
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PW)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials))
    channel = connection.channel()

    # キュー宣言（なければ作成）
    channel.queue_declare(queue='barcode_queue')
    channel.queue_declare(queue='nfc_queue')

    # ハンドラー初期化
    handler = RabbitMQHandler(socketio)

    # イベントバインド
    channel.basic_consume(
        queue='barcode_queue',
        on_message_callback=lambda ch, method, props, body: handler.handle_item(body),
        auto_ack=True)
    channel.basic_consume(
        queue='nfc_queue',
        on_message_callback=lambda ch, method, props, body: handler.handle_user(body),
        auto_ack=True)

    return channel  # 呼び出し元で channel.start_consuming() する
