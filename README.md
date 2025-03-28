# coop

## データベース設計書

本システムは、ユーザが商品を購入するアプリケーションを想定し、以下の4つのテーブルで構成される。注文は「注文全体」と「注文内の個別商品」に分けて記録する設計とし、購入当時の商品の情報も保持できるようにする。

---

### users テーブル（ユーザ情報）

| カラム名 | 型        | 制約     | 説明             |
|----------|-----------|----------|------------------|
| id       | integer   | PK, NN   | ユーザID（主キー）|
| name     | text      | NN       | ユーザ名         |
| grade    | text      | NN       | 学年（例: 20xx年）|
| balance  | integer   | NN       | 所持残高（初期値: 0）|
| nfc_id   | text      | NN       | NFCカードのID    |



### items テーブル（商品情報）

| カラム名  | 型      | 制約   | 説明                        |
|-----------|---------|--------|-----------------------------|
| id        | integer | PK, NN | 商品ID（主キー）           |
| name      | text    | NN     | 商品名                      |
| price     | integer | NN     | 単価（円）                  |
| code      | char(50)| NN     | バーコード                  |
| class     | char(50)| NN     | 商品区分（例: food/drink）  |
| stock_num | integer | NN     | 在庫数                      |



### orders テーブル（注文全体）

| カラム名 | 型        | 制約   | 説明                             |
|----------|-----------|--------|----------------------------------|
| id       | integer   | PK, NN | 注文ID（主キー）                 |
| user_id  | integer   | FK, NN | ユーザID（users.id を参照）      |
| datetime | timestamp | NN     | 注文日時                         |



### order_items テーブル（注文に含まれる商品情報）

| カラム名    | 型        | 制約   | 説明                                       |
|-------------|-----------|--------|--------------------------------------------|
| id          | integer   | PK, NN | 注文商品ID（主キー）                       |
| order_id    | integer   | FK, NN | 注文ID（orders.id を参照）                 |
| item_id     | integer   | FK, NN | 商品ID（items.id を参照）                  |
| item_name   | text      | NN     | 購入時の商品名（スナップショット）         |
| item_price  | integer   | NN     | 購入時の価格（スナップショット）           |
| item_class  | char(50)  | NN     | 購入時の商品区分（スナップショット）       |

---

### 補足

- `orders` と `order_items` は 1対多 の関係。
- `order_items` にスナップショットとして商品情報を保持することで、後から商品情報が変更されても履歴は保持される。
- 将来的に `order_items` に数量（`quantity`）を追加することで、同じ商品を複数個購入するケースにも対応可能。