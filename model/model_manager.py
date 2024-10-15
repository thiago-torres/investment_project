import sqlite3
import pandas as pd

class ModelManager:
    def __init__(self):
        self.conn = sqlite3.connect('model/investments.db')
    
    def close(self):
        self.conn.close()

    def get_assets(self, search_term=None):
        if search_term:
            print(search_term)
            query = "SELECT * FROM assets WHERE asset_name LIKE ? OR asset_type LIKE ?"
            params = (f'%{search_term}%', f'%{search_term}%')
            return self.fetch_query(query, params)
        else:
            return self.fetch_query("SELECT * FROM assets")

    def get_transactions(self, search_term=None):
        if search_term:
            query = "SELECT * FROM transactions WHERE asset_name LIKE ? OR broker LIKE ? OR transaction_type LIKE ? OR asset_type LIKE ?"
            params = (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
            return self.fetch_query(query, params)
        else:
            return self.fetch_query("SELECT * FROM transactions")

    def fetch_query(self, query, params=()):
        return pd.read_sql_query(query, self.conn, params=params)
    

    def insert_transaction(self, broker, date, asset_type, asset_name, transaction_type, quantity, unit_price, fee):
        
        query = '''
            INSERT INTO transactions (broker, date, asset_type, asset_name, transaction_type, quantity, unit_price, fee)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute_query(query, (broker, date, asset_type, asset_name, transaction_type, quantity, unit_price, fee))

    def execute_query(self, query, params=()):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)