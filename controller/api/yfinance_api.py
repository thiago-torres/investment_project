import yfinance as yf

def download_yfinance_data(tickers, start_date, interval='1d'):
    if isinstance(tickers, str):
        tickers = [tickers]

    tickers = [ticker + '.SA' if not ticker.endswith('.SA') else ticker for ticker in tickers]
    
    tickers_down = ','.join(tickers)

    try:
        return yf.download(tickers=tickers_down, start=start_date, progress=False, interval=interval)
    except Exception as e:
        print(f"Yfinance download error for {tickers_down}: {e}")
        return None
