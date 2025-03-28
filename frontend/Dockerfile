FROM node:lts-alpine

WORKDIR /usr/src/app

# package.json のみを先にコピー（ビルドキャッシュを利用）
COPY package.json package-lock.json ./

# 必要なパッケージをインストール
RUN npm install && npm install socket.io-client

# アプリのソースコードをコピー
COPY . .

# アプリを起動
CMD ["npm", "run", "start"]