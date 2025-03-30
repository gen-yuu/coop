-- ユーザ情報
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ユーザID',
    name TEXT NOT NULL COMMENT 'ユーザ名',
    grade TEXT NOT NULL COMMENT '学年',
    balance INT NOT NULL DEFAULT 0 COMMENT '残高',
    nfc_id TEXT NOT NULL COMMENT 'NFCカードID'
) COMMENT='ユーザ情報';

-- 商品情報
CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '商品ID',
    name TEXT NOT NULL COMMENT '商品名',
    price INT NOT NULL COMMENT '価格',
    code CHAR(50) NOT NULL COMMENT 'バーコード',
    class CHAR(50) NOT NULL COMMENT '商品区分',
    stock_num INT NOT NULL COMMENT '在庫数'
) COMMENT='商品情報';

-- 注文情報
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '注文ID',
    user_id INT NOT NULL COMMENT 'ユーザID（外部キー）',
    datetime TIMESTAMP NOT NULL COMMENT '注文日時',
    FOREIGN KEY (user_id) REFERENCES users(id)
) COMMENT='注文情報';

-- 注文商品情報
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '注文商品ID',
    order_id INT NOT NULL COMMENT '注文ID（外部キー）',
    item_id INT NOT NULL COMMENT '商品ID（外部キー）',
    item_name TEXT NOT NULL COMMENT '購入時の商品名（スナップショット）',
    item_price INT NOT NULL COMMENT '購入時の価格',
    item_class CHAR(50) NOT NULL COMMENT '購入時の商品区分',
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (item_id) REFERENCES items(id)
) COMMENT='注文商品情報';