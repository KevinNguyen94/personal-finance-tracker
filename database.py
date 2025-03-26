from datetime import datetime
import sqlite3
import csv

import pandas as pd

# Connect sqlite and Create transaction table 
def create_transaction_table():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            type TEXT,
            amount REAL,
            category TEXT,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

def clear_transaction_table():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions;")
    conn.commit()
    conn.close()

def add_transaction(date, trans_type, amount, category, description):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (date, type, amount, category, description) VALUES (?, ?, ?, ?, ?)",
                   (date, trans_type, amount, category, description))
    conn.commit()
    conn.close()

def print_all_transactions():
    conn = sqlite3.connect("transactions.db")
    df = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()

    pd.set_option('display.max_rows', None)  # Show all rows
    # pd.set_option('display.max_columns', None)  # Show all columns

    print(df)
    
def run_query(query):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute(query)
    transactions = cursor.fetchall()
    conn.commit()
    conn.close()

    for t in transactions:
        print(t)

def get_expenses_by_category():

    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type = 'Expense' GROUP BY category")
    data = dict(cursor.fetchall())  # Convert list of tuples to dictionary
    conn.close()
    return data

def insert_data_csv_to_sqlite():
    filename = 'transactions.csv'
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            add_transaction(row['Date'], row['Type'],row['Amount'],row['Category'],row['Description'])