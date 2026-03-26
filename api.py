from flask import Flask, request, jsonify
app = Flask(__name__)

from models import create_user, add_product, get_products, get_top_products

from services import place_order

def format_products(products):
    return [ {
        "id" : p[0],
        "name" : p[1],
        "price" : float(p[2]),
        "stock" : p[3]
    }
    for p in products
    ]

@app.route("/")
def home():
    return "API is running 😁👌"

@app.route("/users", methods = ["POST"])
def add_user():
    data = request.json
    create_user(data["first_name"], data["last_name"])
    return jsonify({"message" : "User created "})

@app.route("/products", methods = ["POST"])
def add_new_products():
    data = request.json
    add_product(data["name"], data["price"], data["stock"])
    return jsonify({"message" : "Product added"})

@app.route("/products", methods = ["GET"])
def list_products():
    products = get_products()
    return jsonify(format_products(products))

@app.route("/orders", methods = ["POST"])
def create_order():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        user_id = data.get("user_id")
        items = data.get("items")

        if not user_id or not items:
            return jsonify({"error": "Missing user_id or items"}), 400

        if not isinstance(items, list) or len(items) == 0:
            return jsonify({"error": "Items list must not be empty"}), 400

        result, status_code = place_order(user_id, items)
        return jsonify(result), status_code

    except Exception as e:
        print("🔥 ROUTE ERROR:", str(e))
        return jsonify({"error": "Something went wrong"}), 500

@app.route("/analytics/top-products", methods = ["GET"])
def top_products():
    data = get_top_products()
    return jsonify(data)

if __name__ == "__main__":
    app.run()