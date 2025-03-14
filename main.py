import csv
from datetime import datetime

#Reading from a CSV file
def load_transactions(filename):
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
def add_new_transaction(filename):
    new_transaction = {
        'Date': datetime.now().strftime('%Y-%m-%d'),
        'Type': input('Enter transaction type (Income/Expense): '),
        'Category': input('Enter transaction category: '),
        'Amount': float(input('Enter transaction amount: ')),
        'Description': input('Enter transaction description: ')
    }

    with open(filename, mode='a', newline='') as csvfile:
        fieldnames = ['Date', 'Type', 'Category', 'Description', 'Amount']
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
    transactions = load_transactions('transactions.csv')

    for transaction in transactions:
        if transaction['Type'] == 'Income':
            total_income += transaction['Amount']
        else:
            total_expense += transaction['Amount']
    print(f'Total Income: {total_income}')
    print(f'Total Expense: {total_expense}')

if __name__ == '__main__':
    sumerize_transactions('transactions.csv')