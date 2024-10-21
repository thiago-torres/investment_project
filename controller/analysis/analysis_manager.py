from controller.api.yfinance_api import download_yfinance_data
from controller.api.mb_api import MercadoBitcoinPublicData
from controller.analysis.calculate_indicators import calculate_indicators
from controller.analysis.calculate_indicators import calculate_fibonacci_retracement

import pandas as pd
import time
from datetime import datetime, timedelta
import requests

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
                print(self.asset_hour)
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
                        "Ticker":ticker,
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
            return analized_assets

        elif assets["library"] == "mb":
            api = MercadoBitcoinPublicData()

            for ticker in assets['tickers']:
                self.asset_week = api.get_candles(symbol=ticker,resolution="1w",start=assets["start_date"])
                self.asset_week = pd.DataFrame(self.asset_week)
                self.asset_week['c'] = list(map(float, self.asset_week['c']))

                self.asset_day = api.get_candles(symbol=ticker,resolution="1d",start="1696129200")
                self.asset_day = pd.DataFrame(self.asset_day)
                self.asset_day['c'] = list(map(float, self.asset_day['c']))

                self.asset_hour = api.get_candles(symbol=ticker,resolution="1h",start="1728878400") 
                self.asset_hour['c'] = list(map(float, self.asset_hour['c']))   
                self.asset_hour = pd.DataFrame(self.asset_hour)                

                if not self.asset_hour['c'].empty:
                    self.asset_currently = self.asset_hour['c'].iloc[-1]
                else:
                    print(f"Data for {ticker} is empty. Skipping this asset.")

                if self.asset_currently is None:
                    continue

                self.asset_week.rename(columns={'c': 'Adj Close'}, inplace=True)
                self.asset_day.rename(columns={'c': 'Adj Close'}, inplace=True)
                self.asset_hour.rename(columns={'c': 'Adj Close'}, inplace=True)

                self.asset_week = calculate_indicators(df=self.asset_week)
                self.asset_day = calculate_indicators(df=self.asset_day)
                self.asset_hour = calculate_indicators(df=self.asset_hour)

                fibonacci_levels = calculate_fibonacci_retracement(self.asset_week)

                analized_ticker = pd.DataFrame(
                    {
                        "Ticker": ticker,
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
            return analized_assets

        elif assets["library"] == "coinalyze":
            print("coinanalyze off")

    def analysis_personal_assets(self, tickers):
        last_prices = []  
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }

        for ticker in tickers:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}.SA?range=1d&interval=1d"
            
            try:
                # Tenta primeira API (Yahoo Finance)
                response = requests.get(url=url, headers=headers)

                if response.status_code == 200:
                    last_prices.append(response.json()['chart']["result"][0]['indicators']['quote'][0]['close'][0])
                else:
                    print(f'Request to Yahoo Finance failed with status code: {response.status_code}')
                    
                    # Tenta segunda API (MB)
                    api = MercadoBitcoinPublicData()                    
                    
                    try:
                        response = api.get_tickers(symbols=ticker+"-BRL") 

                        if response:
                            last_prices.append(float(response[0]['last']))
                        else:
                            print(f'Request to MB failed with status code: {response.status_code}')
                            last_prices.append(0)

                    except Exception as e:
                        print(f'An error occurred with MB API: {e}')
                        last_prices.append(0)
            
            except Exception as e:
                print(f'An error occurred with Yahoo Finance API: {e}')
                last_prices.append(0)

        return last_prices
