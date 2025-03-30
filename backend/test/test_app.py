import sys
import os

# backend ディレクトリをモジュールパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from consumers.rabbitmq_handler import RabbitMQHandler


@pytest.fixture
def socketio_mock():
    return MagicMock()


@pytest.fixture
def handler(socketio_mock):
    return RabbitMQHandler(socketio_mock)


# --- 商品テスト（バーコード：該当あり） ---
@patch("consumers.rabbitmq_handler.get_item_by_barcode")
def test_handle_item_found(mock_get_item, handler, socketio_mock):
    item = {
        "id": 1,
        "name": "烏龍茶",
        "price": 100,
        "code": "112468",
        "class": "drink",
        "stock_num": 2
    }
    mock_get_item.return_value = item

    handler.handle_item(b"112468")

    socketio_mock.emit.assert_called_once_with("item_registered", item)


# --- 商品テスト（バーコード：該当なし） ---
@patch("consumers.rabbitmq_handler.get_item_by_barcode")
def test_handle_item_not_found(mock_get_item, handler, socketio_mock):
    mock_get_item.return_value = None

    handler.handle_item(b"999999")

    socketio_mock.emit.assert_called_once_with("item_not_found", {"code": "999999"})


# --- ユーザーテスト（NFC：該当あり） ---
@patch("consumers.rabbitmq_handler.get_user_by_nfc_data")
def test_handle_user_found(mock_get_user, handler, socketio_mock):
    user = {"id": 2, "name": "源内裕貴", "grade": "B4", "balance": 0, "nfc_id": "53if95"}
    mock_get_user.return_value = user

    handler.handle_user(b"53if95")

    socketio_mock.emit.assert_called_once_with("user_registered", user)


# --- ユーザーテスト（NFC：該当なし） ---
@patch("consumers.rabbitmq_handler.get_user_by_nfc_data")
def test_handle_user_not_found(mock_get_user, handler, socketio_mock):
    mock_get_user.return_value = None

    handler.handle_user(b"unknown-nfc")

    socketio_mock.emit.assert_called_once_with("user_not_found", {"nfc_id": "unknown-nfc"})
