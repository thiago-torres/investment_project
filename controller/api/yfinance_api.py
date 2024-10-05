import yfinance as yf

def download_yfinance_data(tickers, start_date, interval='1d'):
    try:
        return yf.download(tickers=tickers, start=start_date, progress=False, interval=interval)
    except Exception as e:
        print(f"Yfinance download error for {tickers}: {e}")
        return None