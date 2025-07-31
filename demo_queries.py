import sqlite3

DB_PATH = 'products.db'

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("1. Departments table sample data:")
cur.execute('SELECT * FROM departments LIMIT 5')
for row in cur.fetchall():
    print(dict(row))

print("\n2. Products table sample data (with department_id):")
cur.execute('SELECT id, name, department_id FROM products LIMIT 5')
for row in cur.fetchall():
    print(dict(row))

print("\n3. JOIN query: Products with department names:")
cur.execute('''
    SELECT p.id, p.name, d.name as department_name
    FROM products p
    LEFT JOIN departments d ON p.department_id = d.id
    LIMIT 5
''')
for row in cur.fetchall():
    print(dict(row))

print("\n4. Foreign key relationship demonstration:")
cur.execute('PRAGMA foreign_key_list(products)')
for row in cur.fetchall():
    print(dict(row))

print("\n5. API test: Use /api/products and /api/products/<id> endpoints in browser or curl to confirm department info is included.")

conn.close()
