from controller.analysis.analysis_manager import AnalysisManager
from model.model_manager import ModelManager
from controller.utils.data_utils import load_assets

class ControllerManager():
    def __init__(self):
        self.analysis = AnalysisManager()
        self.selected_assets = None        

    def analysis_global_asset(self, selected):        
        if selected == '1':
            self.selected_assets = load_assets('model/brazilian_stocks.json')            
        elif selected == '2':
            self.selected_assets = load_assets('model/brazilian_reits.json')
        else:
            self.selected_assets = load_assets('model/cryptocurrencies.json')
        print(self.selected_assets)
        return self.analysis.analysis_asset_process(assets=self.selected_assets)
        
    def analysis_my_asset(self, selected, filter):
        db = ModelManager()
        
        if selected == '1':
            if filter != 'cripto':
                self.selected_assets = db.get_assets(filter)
                asset_names = self.selected_assets['ticker'].tolist()

                assets_data = {
                    'library': 'yfinance',
                    'start_date': '2020-01-01',
                    'tickers': asset_names
                }
                
                print(assets_data) 
                return self.analysis.analysis_asset_process(assets=assets_data)
            else:
                self.selected_assets = db.get_assets(filter)
                self.selected_assets['ticker'] = self.selected_assets['ticker']+"-BRL"
                asset_names = self.selected_assets['ticker'].tolist()

                assets_data = {
                    "library":"mb",
                    "start_date": "1665979200",
                    'tickers': asset_names
                }
                
                print(assets_data) 
                return self.analysis.analysis_asset_process(assets=assets_data)
        
        elif selected == '2':
            self.selected_assets = db.get_assets(filter)
            self.selected_assets['atual'] = self.analysis.analysis_personal_assets(self.selected_assets['ticker'])
            self.selected_assets['investido'] = self.selected_assets['cotas'] * self.selected_assets['pm']
            self.selected_assets['valor_atual'] = self.selected_assets['cotas'] * self.selected_assets['atual']
            self.selected_assets['variacao'] = self.selected_assets['valor_atual'] - self.selected_assets['investido']
            return self.selected_assets.round(2)
        else:
            self.selected_assets = db.get_transactions(filter)
            return self.selected_assets
        
    def get_portfolio_chart_data(self):
        db = ModelManager()
        self.selected_assets = db.get_assets()
        self.selected_assets['investido'] = self.selected_assets['cotas'] * self.selected_assets['pm']

        grouped_data = self.selected_assets.groupby('tipo')['investido'].sum()
        total_invest = grouped_data.sum()

        percentage = (grouped_data / total_invest * 100).round(2)

        data = {
            "labels": list(percentage.index),
            "values": list(grouped_data.values.round(2)),
            "percentage": list(percentage.values)
        }
        return data

    def insert_db_transaction(self, corretora, data, tipo, ticker, transacao, cotas, preco_unitario, taxa):
        db = ModelManager()
        return db.insert_transaction(corretora, data, tipo, ticker, transacao, cotas, preco_unitario, taxa)