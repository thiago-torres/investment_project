from controller.controller_manager import ControllerManager
from view.utils import get_user_asset_selection
from view.utils import link_tradingview
from view.utils import style_dataframe

from IPython.display import clear_output, HTML, display

class ViewManager():
    def __init__(self):
        self.controller = ControllerManager()
        self.analyzed_assets = None

    def get_analysis_asset(self):
        assets = get_user_asset_selection()
        clear_output(wait=True)

        if assets != '4':          
            self.analyzed_assets = self.controller.analysis_asset(assets)
            self.display_assets()
        else:
            return 'canceled'     

    def display_assets(self):
        if self.analyzed_assets is not None and not self.analyzed_assets.empty:
            self.analyzed_assets = self.analyzed_assets.sort_values(by='RSI Week')
            self.analyzed_assets.index = [link_tradingview(ticker) for ticker in self.analyzed_assets.index]

            styled_df = style_dataframe(self.analyzed_assets)
            display(HTML(styled_df.to_html(escape=False))) 