#!/bin/bash

# .env 読み込み
ENV_FILE="../.env"
if [ -f "$ENV_FILE" ]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
else
  echo "❌ .env ファイルが見つかりません: $ENV_FILE"
  echo "初期値の環境変数を使用"
fi

DB_CONTAINER=${DB_HOST:-db}
DB_NAME=${DB_NAME:-test_database}
DB_USER=root
DB_PASS=${DB_ROOT_PW:-root}

echo "🧾 テーブル一覧と詳細構造（$DB_NAME）"

# テーブル一覧を取得
tables=$(docker exec -i "$DB_CONTAINER" mysql -u"$DB_USER" -p"$DB_PASS" -N -e "SHOW TABLES IN $DB_NAME")

for table in $tables; do
  echo ""
  echo "🧩 Table: $table"
  echo "----------------------------"
  docker exec -i "$DB_CONTAINER" mysql -u"$DB_USER" -p"$DB_PASS" -D "$DB_NAME" -e "SHOW FULL COLUMNS FROM $table"
done