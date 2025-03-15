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
        'Amount': float(input('Enter transaction amount: ')),
        'Category': input('Enter transaction category: '),
        'Description': input('Enter transaction description: ')
    }

    with open(filename, mode='a', newline='') as csvfile:
        fieldnames = ['Date', 'Type', 'Amount', 'Category', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Only write the header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(new_transaction)

#Sumerize transactions total income and total expense
def sumerize_transactions(transactions):
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

def get_expenses_by_category(transactions):
    expenses = defaultdict(float)
    for transaction in transactions:
        if transaction['Type'] == 'Expense':
            expenses[transaction['Category']] += transaction['Amount']
    return expenses

def get_income_by_category(transactions):
    income = defaultdict(float)
    for transaction in transactions:
        if transaction["Type"] == "Income":
            income[transaction['Category']] += transaction['Amount']
    return income

# Plot bar chart
def plot_expenses(type):
    transactions = load_transactions()

    if type == 'Income':
        expenses = get_income_by_category(transactions)
    elif type == 'Expense':
        expenses = get_expenses_by_category(transactions)

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
    
if __name__ == '__main__':
    plot_expenses("Income")