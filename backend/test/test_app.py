import pytest
from app import on_rabbitmq_message_item, on_rabbitmq_message_user
from flask_socketio import SocketIOTestClient
from flask import Flask
from unittest.mock import patch

# テスト用の Flask アプリと SocketIO クライアントをセットアップ
@pytest.fixture
def test_client():
    app = Flask(__name__)
    socketio = SocketIOTestClient(app)
    return socketio

# 商品テスト（バーコード）
@patch("db_api.database.get_product_by_barcode")
def test_on_rabbitmq_message_item_found(mock_get_product, test_client):
    mock_get_product.return_value = {
        "id": 1,
        "name": "烏龍茶",
        "price": 100,
        "code": "112468",
        "class": "drink",
        "stock_num": 2
    }

    body = b"112468"
    on_rabbitmq_message_item(body)  # Emit 実行される

    # エミットされた内容を検証したい場合は socketio テストクライアントに依存する（別テストで確認）

# ユーザーテスト（NFC）
@patch("db_api.database.get_user_by_nfc_data")
def test_on_rabbitmq_message_user_found(mock_get_user, test_client):
    mock_get_user.return_value = {
        "id": 2,
        "name": "源内裕貴",
        "grade": "B4",
        "balance": 0,
        "nfc_id": "53if95"
    }

    body = b"53if95"
    on_rabbitmq_message_user(body)

# 該当なしパターン（商品）
@patch("db_api.database.get_product_by_barcode")
def test_on_rabbitmq_message_item_not_found(mock_get_product, test_client):
    mock_get_product.return_value = None
    body = b"999999"
    on_rabbitmq_message_item(body)

# 該当なしパターン（ユーザー）
@patch("db_api.database.get_user_by_nfc_data")
def test_on_rabbitmq_message_user_not_found(mock_get_user, test_client):
    mock_get_user.return_value = None
    body = b"unknown-nfc"
    on_rabbitmq_message_user(body)