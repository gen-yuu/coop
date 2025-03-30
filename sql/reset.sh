#!/bin/bash

# 読み込む環境変数ファイル
ENV_FILE="../.env"

# .env を読み込む
if [ -f "$ENV_FILE" ]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
else
  echo "❌ .env ファイルが見つかりません: $ENV_FILE"
  echo "初期値の環境変数を使用"
fi

# 各種設定（.env の値を使用）
DB_CONTAINER=${DB_HOST:-db}
DB_NAME=${DB_NAME:-test_database}
DB_USER=root
DB_PASS=${DB_ROOT_PW:-root}

echo "🌀 Seeding test data into MySQL container: $DB_CONTAINER"

# SQLファイルを順に流し込む
for file in ./seed/*.sql; do
  echo "📥 Importing: $file"
  docker exec -i "$DB_CONTAINER" mysql -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" < "$file"
done

echo "✅ データ投入完了！"