import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from flask import Flask
from flask_socketio import SocketIO
from unittest.mock import patch
from app import on_rabbitmq_message_item, on_rabbitmq_message_user


# --- Flask アプリと SocketIO の初期化（必要に応じて使用） ---
@pytest.fixture
def app():
    app = Flask(__name__)
    socketio = SocketIO(app, async_mode='threading')
    return app


# --- 商品テスト（バーコード：該当あり） ---
@patch("app.socketio.emit")
@patch("app.get_product_by_barcode")
def test_on_rabbitmq_message_item_found(mock_get_product, mock_emit):
    product = {
        "id": 1,
        "name": "烏龍茶",
        "price": 100,
        "code": "112468",
        "class": "drink",
        "stock_num": 2
    }
    mock_get_product.return_value = product

    body = b"112468"
    on_rabbitmq_message_item(body)

    expected_emit_data = product  # または app.py 側と一致する dict を再定義
    mock_emit.assert_called_once_with("item_registered", expected_emit_data)


# --- 商品テスト（バーコード：該当なし） ---
@patch("app.socketio.emit")
@patch("app.get_product_by_barcode")
def test_on_rabbitmq_message_item_not_found(mock_get_product, mock_emit):
    mock_get_product.return_value = None

    body = b"999999"
    on_rabbitmq_message_item(body)

    mock_emit.assert_called_once_with("item_not_found", {"code": "999999"})


# --- ユーザーテスト（NFC：該当あり） ---
@patch("app.socketio.emit")
@patch("app.get_user_by_nfc_data")
def test_on_rabbitmq_message_user_found(mock_get_user, mock_emit):
    user = {"id": 2, "name": "源内裕貴", "grade": "B4", "balance": 0, "nfc_id": "53if95"}
    mock_get_user.return_value = user
    body = b"53if95"
    on_rabbitmq_message_user(body)

    mock_emit.assert_called_once_with("user_registered", user)


# --- ユーザーテスト（NFC：該当なし） ---
@patch("app.socketio.emit")
@patch("app.get_user_by_nfc_data")
def test_on_rabbitmq_message_user_not_found(mock_get_user, mock_emit):
    mock_get_user.return_value = None

    body = b"unknown-nfc"
    on_rabbitmq_message_user(body)

    mock_emit.assert_called_once_with("user_not_found", {"nfc_id": "unknown-nfc"})
