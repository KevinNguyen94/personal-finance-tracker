import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

#Reading from a CSV file
def load_transactions():
    filename = 'transactions.csv'
    transactions = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert date string to datetime object
            row['Date'] = datetime.strptime(row['Date'], '%Y-%m-%d')
            # Convert Amount to float
            row['Amount'] = float(row['Amount'])
            transactions.append(row)
    return transactions

#Adding new transactions
def add_new_transaction():
    filename = 'transactions.csv'
    new_transaction = {
        'Date': datetime.now().strftime('%Y-%m-%d'),
        'Type': input('Enter transaction type (Income/Expense): '),
        'Category': input('Enter transaction category: '),
        'Description': input('Enter transaction description: '),
        'Amount': float(input('Enter transaction amount: '))
    }

    with open(filename, mode='a', newline='') as csvfile:
        fieldnames = ['Date', 'Type', 'Amount', 'Category', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Only write the header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(new_transaction)

#Sumerize transactions total income and total expense
def print_total_income_and_expense():
    total_income = 0
    total_expense = 0

    #Load transactions from a CSV file
    transactions = load_transactions()

    for transaction in transactions:
        if transaction['Type'] == 'Income':
            total_income += transaction['Amount']
        elif transaction['Type'] == 'Expense':
            total_expense += transaction['Amount']

    print(f'Total Income: {total_income:.2f}')
    print(f'Total Expense: {total_expense:.2f}')

def get_expenses_by_category():
    transactions = load_transactions()
    expenses = defaultdict(float)
    for transaction in transactions:
        if transaction['Type'] == 'Expense':
            expenses[transaction['Category']] += transaction['Amount']
    return expenses

def get_income_by_category():
    transactions = load_transactions()
    income = defaultdict(float)
    for transaction in transactions:
        if transaction["Type"] == "Income":
            income[transaction['Category']] += transaction['Amount']
    return income

# Plot bar chart
def plot_bar_chart(type):
    if type == 'Income':
        expenses = get_income_by_category()
    elif type == 'Expense':
        expenses = get_expenses_by_category()

    categories = list(expenses.keys())
    amounts = list(expenses.values())
    
    plt.figure(figsize=(10, 5))
    plt.bar(categories, amounts, color='skyblue')
    if type == 'Income':
        plt.title('Income by Category')
    elif type == 'Expense':
        plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Plot pie chart    
def plot_pie_chart(type):
    if type == 'Income':
        expenses = get_income_by_category()
    elif type == 'Expense':
        expenses = get_expenses_by_category()
    plt.figure(figsize=(7, 7))
    plt.pie(expenses.values(), labels=expenses.keys(), autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=140)
    plt.title("Income Distribution by Category" if type == 'Income' else "Spending Distribution by Category")
    plt.show()    

# Plot line chart

def print_transactions():
    transactions = load_transactions()

    #print headers
    # with open('transactions.csv', newline='') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for header in reader.fieldnames:
    #         print(header, end=' | ')
    for transaction in transactions:
        print(f"\nDate: {transaction['Date'].strftime('%Y-%m-%d')} | Type: {transaction['Type']} | Amount: {transaction['Amount']} | Category: {transaction['Category']} | Description: {transaction['Description']}", end='')
    
def print_menu():

    choice = 0
    while choice != 6:
        print("""
        Personal Finance Tracker Menu:
        1. Add New Transaction
        2. View All Transactions
        3. View Total Income and Expense
        4. Plot Expenses by Category
        5. Plot Income by Category
        6. Exit
        """)
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            add_new_transaction()
        elif choice == '2':
            print_transactions()
        elif choice == '3':
            print_total_income_and_expense()
        elif choice == '4':
            pass
        elif choice == '5':
            pass
        elif choice == '6':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
def get_expenses_over_time():
    transactions = load_transactions()
    daily_expenses = defaultdict(float)
    for transaction in transactions:
        if transaction["Type"] == "Expense":
            date = transaction["Date"]
            daily_expenses[date] += transaction["Amount"]

    sorted_dates = sorted(daily_expenses.keys())
    sorted_amounts = [daily_expenses[date] for date in sorted_dates]

    return sorted_dates, sorted_amounts

def plot_expenses_over_time():
    dates, amounts = get_expenses_over_time()
    
    plt.figure(figsize=(20, 5))
    plt.plot(dates, amounts, marker='o', linestyle='-', color='red')
    plt.title("Expenses Over Time")
    plt.xlabel("Date")
    plt.ylabel("Amount ($)")
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

def get_income_expense_summary():
    transactions = load_transactions()
    income, expense = 0, 0
    for transaction in transactions:
        if transaction["Type"] == "Income":
            income += transaction["Amount"]
        elif transaction["Type"] == "Expense":
            expense += transaction["Amount"]
    return income, expense

def plot_income_vs_expense():
    income, expense = get_income_expense_summary()
    
    categories = ["Income", "Expense"]
    values = [income, expense]

    plt.figure(figsize=(6, 6))
    plt.bar(categories, values, color=["green", "red"])
    plt.title("Income vs. Expenses")
    plt.ylabel("Amount ($)")
    plt.show()


if __name__ == '__main__':
    pass
