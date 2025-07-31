import sqlite3
import csv

# Database and CSV paths
DB_PATH = 'products.db'
CSV_PATH = 'products.csv'

# Table creation SQL
CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    cost REAL,
    category TEXT,
    name TEXT,
    brand TEXT,
    retail_price REAL,
    department TEXT,
    sku TEXT,
    distribution_center_id INTEGER
);
'''

# Load CSV and insert into DB
def load_csv_to_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [(
            int(row['id']),
            float(row['cost']),
            row['category'],
            row['name'],
            row['brand'],
            float(row['retail_price']),
            row['department'],
            row['sku'],
            int(row['distribution_center_id'])
        ) for row in reader]
    cur.executemany('''
        INSERT OR REPLACE INTO products
        (id, cost, category, name, brand, retail_price, department, sku, distribution_center_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', rows)
    conn.commit()
    conn.close()

# Verify import
def verify_import():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT * FROM products LIMIT 10')
    for row in cur.fetchall():
        print(row)
    conn.close()

if __name__ == '__main__':
    load_csv_to_db()
    print('First 10 rows:')
    verify_import()
