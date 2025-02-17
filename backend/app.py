from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ReactとFlaskが別サーバーならCORSを有効化

@app.route("/api/cart")
def get_cart():
    return jsonify({
        "items": [
            {"name": "りんご", "price": 200},
            {"name": "バナナ", "price": 100}
        ],
        "total": 300
    })

@app.route("/api/card")
def get_card():
    return jsonify({"card_number": "****-****-****-1234"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)