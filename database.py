import sqlite3

# Connect to SQLite (or create it)
conn = sqlite3.connect("transactions.db")
cursor = conn.cursor()

# Create a table for transactions
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

# Commit changes & close connection
conn.commit()
conn.close()

def add_transaction(date, trans_type, amount, category, description):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (date, type, amount, category, description) VALUES (?, ?, ?, ?, ?)",
                   (date, trans_type, amount, category, description))
    conn.commit()
    conn.close()

def run_query(query):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute(query)
    transactions = cursor.fetchall()
    conn.commit()
    conn.close()

    for t in transactions:
        print(t)