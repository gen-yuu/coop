import os
from dotenv import load_dotenv

# .env を読み込む（Docker以外の開発環境で有効）
load_dotenv()


class Config:
    # RabbitMQ
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PW = os.getenv("RABBITMQ_PW", "guest")

    # Flask / SocketIO
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "*")

    # その他設定があれば追加可能
