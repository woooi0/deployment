from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

from models import create_user, add_product, get_products, get_top_products
from services import place_order

def format_products(products):
    return[{
        "id": p[0],
        "name": p[1],
        "price": float(p[2]),
        "stock": p[3]
    } for p in products]
@app.route("/")
def home():
    return "API is running 😁👌"

@app.route("/users", methods = ["POST"])
def add_user():
    try:
        data = request.json
        success = create_user(data["first_name"], data["last_name"])
        if success:
            return jsonify({"message" : "User created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create user"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/products", methods = ["POST"])
def add_new_products():
    try:
        data = request.json
        success = add_product(data["name"], data["price"], data["stock"])
        if success:
            return jsonify({"message" : "Product added successfully"}), 201
        else:
            return jsonify({"error" : "Failed to add product"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/products", methods = ["GET"])
def list_products():
    try:
        products = get_products()
        return jsonify(format_products(products))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/orders", methods = ["POST"])
def create_order():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        user_id = data.get("user_id")
        items = data.get("items")

        if not user_id :
            return jsonify({"error": "Missing user_id"}), 400

        if not items :
            return jsonify({"error": "Missing items"}), 400

        if not isinstance(items, list):
            return jsonify({"error": "Items must be a list"}), 400

        for item in items:
            if not isinstance(item, dict):
                return jsonify({"error": "Items must be an object"}), 400
            if "product_id" not in item or "quantity" not in item:
                return jsonify({"error": "Missing product_id and quantity"}), 400

        result, status_code = place_order(user_id, items)
        return jsonify(result), status_code

    except Exception as e:
        print("🔥 ROUTE ERROR:", str(e))
        return jsonify({"error": "Something went wrong"}), 500

@app.route("/analytics/top-products", methods = ["GET"])
def top_products():
    try:
        data = get_top_products()
        formatted_data = []
        for row in data:
            formatted_data.append({
                "product_id": row[0],
                "name": row[1],
                "total_sales": row[2],
                "rank": row[3]
            })
        return jsonify(formatted_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)