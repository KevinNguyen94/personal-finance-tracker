import database
import function

database.clear_transaction_table()
database.insert_data_csv_to_sqlite()
df = database.get_transactions()
# print(df)

database.streamlit_page()