import evdev
from evdev import InputDevice, categorize, ecodes
import pika
import os
import json

# 環境変数から RabbitMQ の接続情報を取得

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PW = os.getenv("RABBITMQ_PW")


# RabbitMQに接続する関数
def create_rabbitmq_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PW)
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials))


def send_barcode_data(barcode_data):
    # # バーコードデータが文字列であることを確認し、バイト型に変換
    if isinstance(barcode_data, str):
        barcode_bytes = barcode_data.encode()

    queue_name = 'barcode_queue' 

    # RabbitMQの接続を作成
    connection = create_rabbitmq_connection()
    channel = connection.channel()

    # キューの作成（存在しない場合のみ作成）
    channel.queue_declare(queue=queue_name)
    # メッセージの送信
    channel.basic_publish(exchange='', routing_key=queue_name, body=barcode_bytes)
    print(f" [x] Sent Barcode data: {barcode_data}")

    connection.close()
    return 0


# テスト
def main():
    print("擬似バーコードデータを入力してください（'exit' で終了）：")
    while True:
        barcode_data = input("> ")  # ユーザーが手動で入力
        if barcode_data.lower() == "exit":
            print("終了します。")
            break
        print(barcode_data)
        send_barcode_data(barcode_data)


# def main():
#     # 利用可能なデバイスをリストアップ
#     devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
#     for device in devices:
#         if 'Barcode' in device.name:
#             # バーコードリーダーのデバイスパスを設定 (例: /dev/input/event0)
#             barcode_scanner_path = device.path

#     # バーコードリーダーデバイスを開く
#     barcode_scanner = InputDevice(barcode_scanner_path)
#     print("バーコードリーダーを監視中...")
#     # バーコードデータを収集するための変数
#     barcode_data = ''
#     while True:
#         for event in barcode_scanner.read_loop():
#             if event.type == ecodes.EV_KEY:
#                 data = categorize(event)
#                 if data.keystate == 1:  # Down events only
#                     if data.keycode == 'KEY_ENTER':
#                         # Enterキーが押されたらバーコードデータを表示してリセット
#                         print("読み取ったバーコード:", barcode_data)
#                         send_barcode_data(barcode_data)
#                         barcode_data = ''
#                     else:
#                         # バーコードデータに文字を追加
#                         barcode_data += data.keycode.lstrip('KEY_')


if __name__ == '__main__':
    main()
