# File: db_utils.py

import sqlite3
import os

DB_NAME = "orders_details.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            products TEXT,
            total_price INTEGER,
            payment_method TEXT,
            payment_status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()

def store_order(name, phone, email, address, products, total_price, payment_method):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO orders (name, phone, email, address, products, total_price, payment_method)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone, email, address, products, total_price, payment_method))
    conn.commit()
    conn.close()

def fetch_all_orders():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM orders ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return data

def update_payment_status(order_id, status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE orders SET payment_status = ? WHERE id = ?", (status, order_id))
    conn.commit()
    conn.close()

def search_order_by_phone(phone):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE phone = ? ORDER BY timestamp DESC", (phone,))
    result = c.fetchall()
    conn.close()
    return result
