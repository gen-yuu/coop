# ベースイメージ（Python 3.9）
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール（evdev用に udev 必要）
RUN apt-get update
RUN apt-get install -y \
    udev \
    && rm -rf /var/lib/apt/lists/*

# 必要なPythonパッケージをインストール
COPY ../barcode_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# バーコードリーダースクリプトをコンテナ内にコピー
COPY ../barcode_service/barcode_service.py .

# コンテナ起動時に実行するコマンド
CMD ["python", "barcode_service.py"]