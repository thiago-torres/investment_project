import sqlite3
import pandas as pd

class ModelManager:
    def __init__(self, db_path='model/investments.db'):
        self.db_path = db_path 

    def fetch_query(self, query, params=()):
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(query, conn, params=params)
        
    def get_assets(self, search_term=None):
        query = "SELECT * FROM ativos"
        params = ()
        if search_term:
            query += " WHERE ticker LIKE ? OR tipo LIKE ?"
            params = (f'%{search_term}%', f'%{search_term}%')
        return self.fetch_query(query, params)

    def get_transactions(self, search_term=None):
        query = "SELECT * FROM transacoes"
        params = ()
        if search_term:
            query += '''
                WHERE ticker LIKE ? OR corretora LIKE ? OR transacao LIKE ? OR tipo LIKE ?
            '''
            params = (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
        return self.fetch_query(query, params)


    def execute_query(self, query, params=()):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()    

    def insert_transaction(self, corretora, data, tipo, ticker, transacao, cotas, preco_unitario, taxa):
        if cotas <= 0:
            return "A quantidade de cotas deve ser maior que zero."
    
        if transacao.lower() == 'sell':
            valid, message = self.is_valid_sell(ticker, cotas, tipo)
            if not valid:
                return message  # Retorna mensagem de "erro" e não insere a transação

        query = '''
            INSERT INTO transacoes (corretora, data, tipo, ticker, transacao, cotas, preco_unitario, taxa)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute_query(query, (corretora, data, tipo, ticker, transacao, cotas, preco_unitario, taxa))

        self.update_or_insert_asset(tipo, ticker, cotas, preco_unitario, transacao)
        
        return "Transação inserida com sucesso!"

    def is_valid_sell(self, ticker, cotas, tipo):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cotas FROM ativos WHERE ticker = ? AND tipo = ?", (ticker,tipo))
            result = cursor.fetchone()
            
            if result:
                cotas_existentes = result[0]
                if cotas_existentes >= cotas:
                    return True, "" 
                else:
                    return False, "Transação de venda superior ao valor disponível do ativo."
            else:
                return False, "Ativo não encontrado."

    def update_or_insert_asset(self, tipo, ticker, cotas, preco_unitario, transacao):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT cotas, pm FROM ativos WHERE ticker = ? AND tipo = ?", (ticker, tipo))
            result = cursor.fetchone()

            if result:
                cotas_existentes, pm_existente = result

                if transacao.lower() == 'buy': 
                    novas_cotas = cotas_existentes + cotas
                    novo_pm = ((cotas_existentes * pm_existente) + (cotas * preco_unitario)) / novas_cotas
                elif transacao.lower() == 'sell':  
                    novas_cotas = cotas_existentes - cotas
                    novo_pm = pm_existente 

                if novas_cotas <= 0:
                    cursor.execute("DELETE FROM ativos WHERE ticker = ? AND tipo = ?", (ticker, tipo))
                else:
                    cursor.execute(
                        "UPDATE ativos SET cotas = ?, pm = ? WHERE ticker = ? AND tipo = ?",
                        (novas_cotas, novo_pm, ticker, tipo)
                    )
            else:
                if transacao.lower() == 'buy':
                    cursor.execute(
                        "INSERT INTO ativos (tipo, ticker, cotas, pm) VALUES (?, ?, ?, ?)",
                        (tipo, ticker, cotas, preco_unitario)
                    )
            conn.commit()

