from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from backend.consumers.rabbitmq_setup import setup_rabbitmq_consumer
from handlers.purchase_handler import register_purchase_handlers
from config import Config

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins=Config.CORS_ALLOWED_ORIGINS, async_mode='threading')

# Socket.IOイベントを登録
register_purchase_handlers(socketio)


def create_app():
    eventlet.spawn(lambda: setup_rabbitmq_consumer(socketio).start_consuming())
    return app


if __name__ == "__main__":
    import eventlet
    eventlet.monkey_patch()
    from eventlet import wsgi
    create_app()
    wsgi.server(eventlet.listen(('0.0.0.0', 8000)), app)
