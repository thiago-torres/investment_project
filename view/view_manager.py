from controller.controller_manager import ControllerManager
from view.utils.display import link_tradingview

class ViewManager():
    def __init__(self):
        self.controller = ControllerManager()
        self.analyzed_assets = None

    def analyze_global_assets(self, selected):
        self.analyzed_assets = self.controller.analysis_global_asset(selected)        
        return self.display_analyzed_assets()

    def analyze_personal_assets(self, selected, filter):
        self.analyzed_assets = self.controller.analysis_my_asset(selected, filter)
        if selected != '1':
            print(self.analyzed_assets)
            return self.analyzed_assets
        else:
            return self.display_analyzed_assets().to_html(escape=False)

    def display_analyzed_assets(self):
        if self.analyzed_assets is not None and not self.analyzed_assets.empty:
            self.analyzed_assets = self.analyzed_assets.sort_values(by='RSI Week')
            self.analyzed_assets["Ticker"] = [link_tradingview(ticker) for ticker in self.analyzed_assets["Ticker"]]
            
            return self.analyzed_assets
        return '<p>Nenhum ativo analisado.</p>'
    
    def get_portfolio_chart_data(self):
        return self.controller.get_portfolio_chart_data()
    
    def insert_db_transaction(self, corretora, data, tipo, ticker, transacao, cotas, preco_unitario, taxa):
        return self.controller.insert_db_transaction(corretora, data, tipo, ticker, transacao, cotas, preco_unitario, taxa)