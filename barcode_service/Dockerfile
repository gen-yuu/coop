##バーコードAPIコンテナ

# ベースイメージ（Python 3.9）
FROM python:3.9

# 作業ディレクトリの設定
WORKDIR /usr/src/app

# 必要なパッケージのインストール（evdev用に udev 必要）
RUN apt-get update
RUN apt-get install -y \
    udev \
    libevdev-dev \
    libudev-dev \
    linux-headers-generic \
    && rm -rf /var/lib/apt/lists/

RUN pip install --upgrade pip setuptools wheel
# 必要なPythonパッケージをインストール
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# evdev を個別にインストール
RUN pip install --no-cache-dir evdev 

# コンテナ起動時に実行するコマンド
# CMD ["python", "barcode_service.py"]