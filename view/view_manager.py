from controller.controller_manager import ControllerManager
from view.utils.selection import get_asset_selection_global, get_asset_selection_personal
from view.utils.display import link_tradingview, style_dataframe

from IPython.display import HTML, display

class ViewManager():
    def __init__(self):
        self.controller = ControllerManager()
        self.analyzed_assets = None

    def analyze_global_assets(self):
        selected = get_asset_selection_global()
        
        if selected != '4':          
            self.analyzed_assets = self.controller.analysis_global_asset(selected)
            self.display_analyzed_assets()
        else:
            return 'canceled'     

    def analyze_personal_assets(self):
        selected = get_asset_selection_personal()

        if selected != '4':          
            self.analyzed_assets = self.controller.analysis_my_asset(selected)
            display(self.analyzed_assets)
            # self.display_analyzed_assets()
        else:
            return 'canceled' 

    def display_analyzed_assets(self):
        if self.analyzed_assets is not None and not self.analyzed_assets.empty:
            self.analyzed_assets = self.analyzed_assets.sort_values(by='RSI Week')
            self.analyzed_assets.index = [link_tradingview(ticker) for ticker in self.analyzed_assets.index]

            styled_df = style_dataframe(self.analyzed_assets)
            display(HTML(styled_df.to_html(escape=False))) 
        