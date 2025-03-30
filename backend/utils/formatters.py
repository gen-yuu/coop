def build_item_info(item):
    return {
        "id": item["id"],
        "name": item["name"],
        "price": item["price"],
        "code": item["code"],
        "class": item["class"],
        "stock_num": item["stock_num"]
    }


def build_user_info(user):
    return {
        "id": user["id"],
        "name": user["name"],
        "grade": user["grade"],
        "balance": user["balance"],
        "nfc_id": user["nfc_id"]
    }
