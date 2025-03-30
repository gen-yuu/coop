from utils.formatters import build_item_info, build_user_info
from db_api.database import get_item_by_barcode, get_user_by_nfc_data


class RabbitMQHandler:

    def __init__(self, socketio):
        self.socketio = socketio

    def handle_item(self, body):
        barcode = body.decode()
        print(f"Received barcode: {barcode}")
        try:
            product = get_item_by_barcode(barcode)
        except Exception as e:
            print(f"DB error: {e}")
            product = None

        if product:
            data = build_item_info(product)
            self.socketio.emit("item_registered", data)
        else:
            self.socketio.emit("item_not_found", {"code": barcode})

    def handle_user(self, body):
        nfc_id = body.decode()
        print(f"Received NFC: {nfc_id}")
        try:
            user = get_user_by_nfc_data(nfc_id)
        except Exception as e:
            print(f"DB error: {e}")
            user = None

        if user:
            data = build_user_info(user)
            self.socketio.emit("user_registered", data)
        else:
            self.socketio.emit("user_not_found", {"nfc_id": nfc_id})
