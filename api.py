from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = 'products.db'

# Helper function to get DB connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------- Departments APIs --------------------

# GET /api/departments - list all departments with product counts
@app.route('/api/departments', methods=['GET'])
def get_departments():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT d.id, d.name, COUNT(p.id) as product_count
            FROM departments d
            LEFT JOIN products p ON d.id = p.department_id
            GROUP BY d.id
        ''')
        departments = [
            {"id": row[0], "name": row[1], "product_count": row[2]}
            for row in cur.fetchall()
        ]
        conn.close()
        return jsonify({"departments": departments})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /api/departments/<id> - Get a single department with its product count
@app.route('/api/departments/<int:dept_id>', methods=['GET'])
def get_department(dept_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name FROM departments WHERE id = ?', (dept_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            return jsonify({"error": "Department not found"}), 404

        cur.execute('SELECT COUNT(*) FROM products WHERE department_id = ?', (dept_id,))
        product_count = cur.fetchone()[0]
        conn.close()
        return jsonify({"id": row[0], "name": row[1], "product_count": product_count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /api/departments/<id>/products - list products in a department
@app.route('/api/departments/<int:dept_id>/products', methods=['GET'])
def get_department_products(dept_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT name FROM departments WHERE id = ?', (dept_id,))
        dept_row = cur.fetchone()
        if not dept_row:
            conn.close()
            return jsonify({"error": "Department not found"}), 404

        department_name = dept_row[0]
        cur.execute('SELECT * FROM products WHERE department_id = ?', (dept_id,))
        products = [dict(row) for row in cur.fetchall()]
        conn.close()
        return jsonify({"department": department_name, "products": products})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- Products APIs --------------------

# GET /api/products - List all products (paginated)
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT COUNT(*) FROM products')
        total = cur.fetchone()[0]

        cur.execute('''
            SELECT p.*, d.name as department_name
            FROM products p
            LEFT JOIN departments d ON p.department_id = d.id
            LIMIT ? OFFSET ?
        ''', (per_page, offset))

        products = []
        for row in cur.fetchall():
            prod = dict(row)
            prod['department'] = prod.pop('department_name', None)
            products.append(prod)

        conn.close()

        return jsonify({
            'products': products,
            'page': page,
            'per_page': per_page,
            'total': total
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# GET /api/products/<id> - Get a specific product by ID
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT p.*, d.name as department_name
            FROM products p
            LEFT JOIN departments d ON p.department_id = d.id
            WHERE p.id = ?
        ''', (product_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            prod = dict(row)
            prod['department'] = prod.pop('department_name', None)
            return jsonify(prod)
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
