import bcrypt
from connect import get_cursor

def login_user(email, password):
    conn, cursor = get_cursor()
    if not conn:
        return None, "Database connection failed"
    try:
        cursor.execute("SELECT id, first_name, last_name, password_hash FROM users WHERE email = %s ", (email,))
        user = cursor.fetchone()
        if not user:
            return None, "User not found"

        user_id, first_name, last_name, stored_hash = user

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return {"id": user_id, "first_name": first_name, "last_name": last_name}, None
        else:
            return None, "Invalid password"
    except Exception as e:
        return None, str(e)
    finally:
        cursor.close()
        conn.close()

def create_user (first_name, last_name, email, password):
    conn, cursor = get_cursor()
    if not conn:
        return False, "Database connection failed"
    try:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (first_name, last_name, email, hashed))
        conn.commit()
        return True, cursor.lastrowid
    except Exception as e:
        conn.rollback()
        return False, str(e)
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

