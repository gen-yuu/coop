# NFCリーダーのコンテナ用Dockerfile
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

#USBデバイスを扱うプログラムをOSを意識せずに扱えるライブラリをインストール
RUN apt-get update
RUN apt install -y \
    libusb-dev\
    python3-usb\
    && rm -rf /var/lib/apt/lists/*

# 依存ライブラリのインストール
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# NFCサービススクリプトをコピー
# COPY ../nfc_service/nfc_service.py .

# スクリプトを実行
# CMD ["python", "nfc_service.py"]