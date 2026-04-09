from connect import get_cursor

def create_user (first_name, last_name):
    conn, cursor = get_cursor()
    if not conn:
        return False
    try:
        query = "INSERT INTO users (first_name, last_name) VALUES (%s, %s)"
        cursor.execute(query, (first_name, last_name))
        conn.commit()
        print("User created successfully")
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def add_product(name,price,stock):
    conn, cursor = get_cursor()
    if not conn:
        return False
    try:
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)", (name, price, stock))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding product: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_products():
    conn, cursor = get_cursor()
    if not conn:
        return []
    try:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        return products
    except Exception as e:
        print(f"Error getting products: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_top_products():
    conn, cursor = get_cursor()
    if not conn:
        return []
    try:
        cursor.execute("""SELECT *, DENSE_RANK() OVER(ORDER BY total_sales DESC) AS rank_num FROM product_sales""")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting top products: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

