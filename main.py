import csv
from datetime import datetime

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

if __name__ == '__main__':
    transactions = load_transactions('transactions.csv')
    for transaction in transactions:
        print(transaction)