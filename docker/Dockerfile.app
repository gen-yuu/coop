# ベースイメージ（Python 3.9）
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app


# 各ライブラリインストール
RUN apt-get update
RUN apt-get install -y \
    vim \
    sudo \
    apache2 

RUN pip install --no-cache-dir -r requirements.txt
CMD ["apache2","-D","FOREGROUND"]

# default.confを修正
RUN rm /etc/apache2/sites-available/000-default.conf
RUN pip install --no-cache-dir -r requirements.txt



