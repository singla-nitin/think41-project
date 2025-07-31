import sqlite3
import csv

DB_PATH = 'products.db'
CSV_PATH = 'products.csv'

def create_departments_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
    ''')
    conn.commit()

def get_unique_departments():
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return sorted(set(row['department'] for row in reader))

def populate_departments(conn, departments):
    for name in departments:
        conn.execute('INSERT OR IGNORE INTO departments (name) VALUES (?)', (name,))
    conn.commit()

def add_department_id_column(conn):
    # Add department_id column if not exists
    cur = conn.execute("PRAGMA table_info(products)")
    columns = [row[1] for row in cur.fetchall()]
    if 'department_id' not in columns:
        conn.execute('ALTER TABLE products ADD COLUMN department_id INTEGER')
        conn.commit()

def update_products_department_id(conn):
    # Map department name to id
    cur = conn.execute('SELECT id, name FROM departments')
    dept_map = {row[1]: row[0] for row in cur.fetchall()}
    cur = conn.execute('SELECT id, department FROM products')
    for prod_id, dept_name in cur.fetchall():
        dept_id = dept_map.get(dept_name)
        if dept_id:
            conn.execute('UPDATE products SET department_id = ? WHERE id = ?', (dept_id, prod_id))
    conn.commit()

def drop_department_column(conn):
    # SQLite does not support DROP COLUMN directly; need to recreate table if desired
    pass  # For now, keep the old column

if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    create_departments_table(conn)
    departments = get_unique_departments()
    populate_departments(conn, departments)
    add_department_id_column(conn)
    update_products_department_id(conn)
    # drop_department_column(conn)  # Optional, not implemented
    conn.close()
