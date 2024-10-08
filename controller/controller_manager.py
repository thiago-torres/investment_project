from controller.analysis.analysis_manager import AnalysisManager
from controller.utils.data_utils import load_assets

class ControllerManager():
    def __init__(self):
        self.analysis = AnalysisManager()
        self.assets = None        

    def analysis_asset(self, assets):        
        if assets == '1':
            self.assets = load_assets('model/brazilian_stocks.json')            
        elif assets == '2':
            self.assets = load_assets('model/brazilian_reits.json')
        else:
            self.assets = load_assets('model/cryptocurrencies.json')

        return self.analysis.analysis_asset_process(assets=self.assets)
        

