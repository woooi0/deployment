from connect import get_connection

def place_order(user_id, items):
    try:
        print("🛑 Starting order.... ")
        with get_connection() as conn:
            if not conn:
                return{"error" : "Database connection failed"}, 500

            cursor = conn.cursor()

            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))

            user = cursor.fetchone()

            if not user:
                print("❌ User Not Found!")
                cursor.close()
                return{"error" : "User not found"}, 404

            for product_id, qty in items:
                print(f" Checking product {product_id} with qty {qty}")

                cursor.execute("SELECT stock, price FROM products WHERE id = %s", (product_id,))

                result = cursor.fetchone()

                if not result:
                    print(f"❌ Product Not Found: {product_id}")
                    cursor.close()
                    return{"error" : f"Product {product_id} not found"}, 404

                stock, price = result
                print(f" Stock : {stock}, Requested : {qty}")

                if qty > stock:
                    print("⚠️ Not Enough Stock ⚠️")
                    cursor.close()
                    return{
                        "error" : f"Not enough stock for product {product_id}",
                        "available_stock" : stock
                    }, 400

            cursor.execute("INSERT INTO orders(user_id) VALUES (%s)", (user_id,))
            order_id = cursor.lastrowid

            for product_id, qty in items:
                cursor.execute("SELECT price FROM products WHERE id = %s", (product_id,))
                price = cursor.fetchone()[0]

                cursor.execute("""INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)"""
                           , (order_id, product_id, qty, price))

                cursor.execute("""UPDATE products SET stock = stock - %s WHERE id = %s""", (qty, product_id))

            conn.commit()
            cursor.close()
            print("✅ Order committed")
            return {
                "message": "Order placed successfully",
                "order_id": order_id
            }, 201

    except Exception as e:
        if 'conn' in locals() and conn:
            conn.rollback()

        print("🔥 ERROR :", str(e))
        return {
            "error": "Internal server error",
            "details": str(e)
        }, 500







