ALTER TABLE order_items
ADD COLUMN quantity INT NOT NULL DEFAULT 1 AFTER item_class;