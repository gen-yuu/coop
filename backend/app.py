from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ReactとFlaskが別サーバーならCORSを有効化

@app.route("/api/item", methods=['GET'])
def get_item():
    return jsonify(
        {"id": 1, "name":"烏龍茶","price":100,"code":"112468","class":"drink","stock_num":2}
    )

@app.route("/api/card")
def get_card():
    return jsonify({"card_number": "****-****-****-1234"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)