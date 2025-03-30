from flask_socketio import SocketIO
from db_api.database import (get_connection, get_user_by_id, get_item_by_id, update_stock,
                             update_balance, insert_order, insert_order_item)


def register_purchase_handlers(socketio: SocketIO):

    @socketio.on("confirm_purchase")
    def handle_confirm_purchase(data):
        # {
        # user_id: 1,
        # items: [
        #     { item_id: 3, quantity: 2 },
        #     { item_id: 8, quantity: 1 }
        # ]
        # }
        user_id = data.get("user_id")
        items = data.get("items", [])

        try:
            total_price = 0
            purchased = []

            user = get_user_by_id(user_id)
            if not user:
                raise ValueError(f"ユーザが見つかりません: {user_id}")

            for entry in items:
                item_id = entry["item_id"]
                qty = entry["quantity"]
                item = get_item_by_id(item_id)

                if not item:
                    raise ValueError(f"商品が見つかりません: {item_id}")
                if item["stock_num"] < qty:
                    raise ValueError(f"在庫不足: {item['name']}")

                total_price += item["price"] * qty
                purchased.append({"item": item, "quantity": qty})

            conn = get_connection()
            try:
                with conn.cursor():
                    order_id = insert_order(user_id, conn=conn)

                    for p in purchased:
                        update_stock(p["item"]["id"], -p["quantity"], conn)
                        insert_order_item(order_id, p["item"], p["quantity"], conn)

                    update_balance(user_id, -total_price, conn)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                conn.close()

            socketio.emit(
                "purchase_complete", {
                    "status": "success",
                    "message": "購入完了",
                    "items": [{
                        "name": p["item"]["name"],
                        "quantity": p["quantity"],
                        "unit_price": p["item"]["price"]
                    } for p in purchased],
                    "total": total_price
                })

        except Exception as e:
            socketio.emit("purchase_complete", {"status": "error", "message": str(e)})
