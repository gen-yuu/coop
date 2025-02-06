# -*- coding: utf-8 -*-
import binascii
import json
import os

import nfc
import pika

# NFCリーダーのID
NFC_READER_ID = "usb:054c:06c3"  # Sony RC-S380

# 環境変数から RabbitMQ の接続情報を取得
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.environ.get("RABBITMQ_PORT"))
RABBITMQ_USER = os.environ.get("RABBITMQ_USER")
RABBITMQ_PW = os.environ.get("RABBITMQ_PASSWORD")


# RabbitMQに接続する関数
def create_rabbitmq_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PW)
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials))


# RabbitMQへNFCデータを送信する関数
def send_nfc_data(channel, nfc_data):
    """
    NFCのデータをRabbitMQのキューに送信する。
    
    - `nfc_data` が文字列の場合は 'nfc_registration' キューに送信
    - JSON形式に変換可能なオブジェクトの場合は 'nfc_queue' キューに送信
    """
    if isinstance(nfc_data, str):
        queue_name = 'nfc_registration'
        nfc_bytes = nfc_data.encode()  # 文字列をバイト列に変換
    else:
        queue_name = 'nfc_queue'
        nfc_bytes = json.dumps(nfc_data).encode()  # JSONに変換してバイト列化

    # キューの作成（存在しない場合のみ作成）
    channel.queue_declare(queue=queue_name)
    # メッセージの送信
    channel.basic_publish(exchange='', routing_key=queue_name, body=nfc_bytes)
    print(f" [x] Sent NFC data: {nfc_bytes}")


# TODO:DB接続
# ユーザー情報を取得するダミー関数
def get_user(idm):
    """
    NFCタグのIDm（識別子）からユーザー情報を取得する。
    実際の環境ではデータベースを参照する形に変更する。
    """
    return {"id": idm, "name": "Test User", "status": "active"}


if __name__ == '__main__':
     while True:
        # NFCリーダーを初期化
        clf = nfc.ContactlessFrontend(NFC_READER_ID)
        # RabbitMQの接続を作成
        connection = create_rabbitmq_connection()
        channel = connection.channel()

        print("NFCリーダーを待機中...")
        # NFCタグの読み取りを試行
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        # タグが正常に取得でき、IDm（識別子）が存在する場合
        if tag and tag.idm:
            idm = binascii.hexlify(tag.idm).decode()  # バイナリを16進文字列に変換
            print(f"NFCタグ検出: {idm}")
            # ユーザー情報を取得
            user_info = get_user(idm)
            # RabbitMQへ送信
            send_nfc_data(channel, user_info)
        else:
            print("無効なNFCタグが検出されました。")
        clf.close()