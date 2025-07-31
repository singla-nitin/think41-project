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

# GET /api/products - List all products (with pagination)
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
            # Replace department field with department_name
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
