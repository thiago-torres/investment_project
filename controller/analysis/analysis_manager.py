from controller.api.yfinance_api import download_yfinance_data
from controller.analysis.calculate_indicators import calculate_indicators
from controller.analysis.calculate_indicators import calculate_fibonacci_retracement

import pandas as pd

class AnalysisManager:
    def __init__(self):
        self.asset_currently = None
        self.asset_hour = None
        self.asset_day = None
        self.asset_week = None

    def analysis_asset_process(self, assets):
        analized_assets = pd.DataFrame()
        print(f"Tamanho do DataFrame: {analized_assets.shape[0]}")
        print(f"Número de tickers: {len(assets['tickers'])}")
                
        if assets["library"] == "yfinance":
            for ticker in assets['tickers']:
                self.asset_week = download_yfinance_data(tickers=ticker, start_date=assets['start_date'], interval='1wk')
                self.asset_day = download_yfinance_data(tickers=ticker, start_date=assets['start_date'])
                self.asset_hour = download_yfinance_data(tickers=ticker, start_date="2024-01-01", interval='1h')
                if not self.asset_hour['Close'].empty:
                    self.asset_currently = self.asset_hour['Close'].iloc[-1]
                else:
                    print(f"Data for {ticker} is empty. Skipping this asset.")


                if self.asset_currently is None:
                    continue

                self.asset_week = calculate_indicators(df=self.asset_week)
                self.asset_day = calculate_indicators(df=self.asset_day)
                self.asset_hour = calculate_indicators(df=self.asset_hour)

                fibonacci_levels = calculate_fibonacci_retracement(self.asset_day)

                analized_ticker = pd.DataFrame(
                    {
                        "Value":self.asset_currently,
                        "EMA 1h":[self.asset_hour['EMA'].iloc[-1]],
                        "EMA Day":[self.asset_day['EMA'].iloc[-1]],
                        "EMA Week":[self.asset_week['EMA'].iloc[-1]],
                        "RSI 1h":[self.asset_hour['RSI'].iloc[-1]],
                        "RSI Day":[self.asset_day['RSI'].iloc[-1]],
                        "RSI Week":[self.asset_week['RSI'].iloc[-1]],
                        **fibonacci_levels                      
                    }
                )
                
                analized_assets = pd.concat([analized_assets,analized_ticker])            

            analized_assets = analized_assets.round(3)
            return analized_assets.set_index([assets['tickers']])



        elif assets["library"] == "coinalyze":
            print("coinanalyze off")
        
