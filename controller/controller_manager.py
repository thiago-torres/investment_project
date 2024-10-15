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
            self.selected_assets = db.get_assets(filter)
            asset_names = self.selected_assets['ticker'].tolist()

            assets_data = {
                'library': 'yfinance',
                'start_date': '2020-01-01',
                'tickers': asset_names
            }
            
            print(assets_data) 
            return self.analysis.analysis_asset_process(assets=assets_data) 
        
        elif selected == '2':
            self.selected_assets = db.get_assets(filter)
        else:
            self.selected_assets = db.get_transactions(filter)
        
        return self.selected_assets