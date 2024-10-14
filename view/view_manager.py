from controller.controller_manager import ControllerManager
from view.utils.display import link_tradingview, style_dataframe

class ViewManager():
    def __init__(self):
        self.controller = ControllerManager()
        self.analyzed_assets = None

    def analyze_global_assets(self, selected):
        self.analyzed_assets = self.controller.analysis_global_asset(selected)
        return self.display_analyzed_assets()

    def analyze_personal_assets(self, selected):
        self.analyzed_assets = self.controller.analysis_my_asset(selected)
        if selected != '1':
            print(self.analyzed_assets)
            return self.analyzed_assets.to_html(escape=False)
        else:
            return self.display_analyzed_assets()

    def display_analyzed_assets(self):
        if self.analyzed_assets is not None and not self.analyzed_assets.empty:
            self.analyzed_assets = self.analyzed_assets.sort_values(by='RSI Week')
            self.analyzed_assets.index = [link_tradingview(ticker) for ticker in self.analyzed_assets.index]
            styled_df = style_dataframe(self.analyzed_assets)
            return styled_df.to_html(escape=False)
        return '<p>Nenhum ativo analisado.</p>'