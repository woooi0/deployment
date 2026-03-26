from connect import get_connection

def create_user (first_name, last_name):
    with get_connection() as conn:
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO users (first_name, last_name) VALUES (%s, %s)"
            cursor.execute(query, (first_name, last_name))
            conn.commit()
            print("User created successfully")
            conn.commit()
            cursor.close()

def add_product(name,price,stock):
    with get_connection() as conn:
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)", (name, price, stock))
            conn.commit()
            cursor.close()

def get_products():
    with get_connection() as conn:
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products")
            results = cursor.fetchall()
            cursor.close()
            return results
    return []

def get_top_products():
    with get_connection() as conn:
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""SELECT *, DENSE_RANK() OVER(ORDER BY total_sales DESC) AS rank_num FROM product_sales""")
            results = cursor.fetchall()
            cursor.close()
            return results
    return []