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
            query = "SELECT * FROM ativos WHERE ticker LIKE ? OR tipo LIKE ?"
            params = (f'%{search_term}%', f'%{search_term}%')
            return self.fetch_query(query, params)
        else:
            return self.fetch_query("SELECT * FROM ativos")

    def get_transactions(self, search_term=None):
        if search_term:
            query = '''
                SELECT * FROM transacoes 
                WHERE ticker LIKE ? OR corretora LIKE ? OR transacao LIKE ? OR tipo LIKE ?
            '''
            params = (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
            return self.fetch_query(query, params)
        else:
            return self.fetch_query("SELECT * FROM transacoes")

    def fetch_query(self, query, params=()):
        return pd.read_sql_query(query, self.conn, params=params)
    
    def insert_transacao(self, corretora, data, tipo_ativo, ticker, transacao, cotas, preco_unitario, taxa):
        query = '''
            INSERT INTO transacoes (corretora, data, tipo, ticker, transacao, cotas, preco_unitario, taxa)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute_query(query, (corretora, data, tipo_ativo, ticker, transacao, cotas, preco_unitario, taxa))

    def execute_query(self, query, params=()):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
