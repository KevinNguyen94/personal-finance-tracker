from datetime import datetime
import sqlite3
import csv
from matplotlib import pyplot as plt
import streamlit as st
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

def get_transactions():
    conn = sqlite3.connect("transactions.db")
    df = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()

    pd.set_option('display.max_rows', None)  # Show all rows
    
    return df
    
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

def draw_expense_income_by_category():
    df = get_transactions()

    # Total Income & Expenses
    total_income = df[df["type"] == "Income"]["amount"].sum()
    total_expense = df[df["type"] == "Expense"]["amount"].sum()
    
    st.metric("💰 Total Income", f"${total_income:.2f}")
    st.metric("💸 Total Expenses", f"${total_expense:.2f}")

    # Dropdown to Select Transaction Type
    filter_type = st.selectbox("Choose type to draw the breakdown", ["Both", "Income", "Expense"], key="select_1")

    if filter_type in ["Both","Expense"]:
        # Expense breakdown by category (Bar chart)
        st.subheader("📊 Expense Breakdown by Category")
        expense_df = df[df["type"] == "Expense"].groupby("category")["amount"].sum()
        st.bar_chart(expense_df)
    if filter_type in ["Both","Income"]:
        # Income breakdown by category (Bar chart)
        st.subheader("📊 Income Breakdown by Category")
        expense_df = df[df["type"] == "Income"].groupby("category")["amount"].sum()
        st.bar_chart(expense_df)

def draw_expense_income_overtime():
    # Load Data from SQLite
    def load_data():
        conn = sqlite3.connect("transactions.db")
        df = pd.read_sql("SELECT date, type, amount FROM transactions", conn)
        conn.close()
        return df

    # Load and Process Data
    df = load_data()
    df["date"] = pd.to_datetime(df["date"])  # Convert to datetime
    df = df.sort_values("date")  # Sort by date

    # Streamlit UI
    st.subheader("📈 Income & Expense Trend Over Time")

    # Date Range Selector
    min_date = df["date"].min()
    max_date = df["date"].max()
    start_date, end_date = st.date_input("Select Date Range", [min_date, max_date])

    # Dropdown to Select Transaction Type
    filter_type = st.selectbox("Filter by Type", ["Both", "Income", "Expense"],key="select_2")

    # Filter Data Based on Selected Dates
    filtered_df = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

    # Apply Type Filter
    if filter_type != "Both":
        filtered_df = filtered_df[filtered_df["type"] == filter_type]

    # Aggregate Income & Expenses
    income = filtered_df[filtered_df["type"] == "Income"].groupby("date")["amount"].sum()
    expenses = filtered_df[filtered_df["type"] == "Expense"].groupby("date")["amount"].sum()
     
    # Plot the Line Chart
    fig, ax = plt.subplots(figsize=(10, 5))

    if filter_type in ["Both", "Income"]:
        ax.plot(income.index, income.values, marker="o", linestyle="-", label="Income", color="green")
    if filter_type in ["Both", "Expense"]:
        ax.plot(expenses.index, expenses.values, marker="o", linestyle="-", label="Expenses", color="red")

    ax.set_xlabel("Date")
    ax.set_ylabel("Amount ($)")
    ax.set_title(f"{filter_type} Over Time")
    ax.legend()
    ax.grid(True)

    # Show the plot in Streamlit
    st.pyplot(fig)



def streamlit_page():
    st.title("📊 Personal Finance Tracker")

    # Display transactions in table
    df = get_transactions()

    if df.empty:
        st.warning("No transactions found. Add data to the database!")
    else:
        st.dataframe(df)  

    draw_expense_income_by_category()
    draw_expense_income_overtime()