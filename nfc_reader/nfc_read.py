# -*- coding: utf-8 -*-
import pika
import nfc
import json
import binascii

#test
from connect_db import get_user

def send_nfc_data(nfc):
    # RabbitMQに接続
    credentials = pika.PlainCredentials("srv-admin", "704lIlac")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", port=5672, credentials=credentials))
    channel = connection.channel()

    if isinstance(nfc, str):
        # NFCデータが文字列であることを確認し、バイト型に変換
        channel.queue_declare(queue='nfc_registration')
        nfc_bytes = nfc.encode()
        channel.basic_publish(exchange='', routing_key='nfc_registration', body=nfc_bytes)
    else:
        # NFCデータがすでにバイト型であるか、またはJSON形式に変換可能なオブジェクトである場合
        channel.queue_declare(queue='nfc_queue')
        nfc_bytes = json.dumps(nfc).encode()
        channel.basic_publish(exchange='', routing_key='nfc_queue', body=nfc_bytes)
    print(f" [x] Sent NFC data: {nfc_bytes}")
    connection.close()

if __name__ == '__main__':
    NFC_READER_ID = "usb:054c:06c3" # Sony RC-S380
    while True:
        clf = nfc.ContactlessFrontend(NFC_READER_ID)
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        idm = binascii.hexlify(tag.idm)
        if idm!= 0:
            # IDmは16進表記
            print(idm)
            user_info = get_user(idm.decode())
            send_nfc_data(user_info)
        clf.close()