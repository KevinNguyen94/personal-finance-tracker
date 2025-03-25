import database
import function

database.add_transaction("2025-03-10", "Expense", 45.00, "Dining", "Dinner with friends")
database.run_query("SELECT * FROM transactions")
