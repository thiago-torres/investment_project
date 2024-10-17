import pandas as pd

def link_tradingview(ticker):
    if isinstance(ticker, tuple):
        ticker = ticker[0]  # Extrai o ticker se for uma tupla
    
    # link2 referente ao gráfico do coinalyze será habilitado no futuro precisará criar uma lista para checar o nome completo do ativo por exemplo BTC=bitcoin

    if ticker == 'USD/BRL':
        return f'<a href="https://br.tradingview.com/chart/JKfvODlT/?symbol=FX_IDC%3AUSDBRL" target="_blank">{ticker}</a>'
    
    elif ticker == 'BTCDOMUSDT_PERP.A':
        link1 = f'<a href="https://br.tradingview.com/chart/JKfvODlT/?symbol=BITFINEX%3ABTCDOMUST.P" target="_blank">DOM-BTC</a>'
        # link2 = f'<a href="https://br.coinalyze.net/binance-btcdom-index/usdt/binance/btcdomusdt_perp/price-chart-live/?tab=watchlists" target="_blank">DOM-BTC</a>'
        return link1 # return f'{link1} | {link2}'
    
    elif ticker.endswith('_PERP.A'):
        ticker_base = ticker.replace('USDT_PERP.A', '')
        link1 = f'<a href="https://br.tradingview.com/chart/JKfvODlT/?symbol=BINANCE%3A{ticker_base}USDT" target="_blank">{ticker_base}USDT</a>'
        # link2 = f'<a href="https://br.coinalyze.net/{nome_cripto_por_extenso(ticker_base.lower())}/usdt/binance/{ticker_base.lower()}usdt_perp/price-chart-live/?tab=watchlists" target="_blank">{ticker_base}USDT</a>'
        return link1
    
    elif ticker.endswith('-BRL'):
        ticker_base = ticker.replace('-BRL', '')
        link1 = f'<a href="https://br.tradingview.com/chart/JKfvODlT/?symbol=BINANCE%3A{ticker_base}USDT" target="_blank">{ticker_base}USDT</a>'
        # link2 = f'<a href="https://br.coinalyze.net/{nome_cripto_por_extenso(ticker_base.lower())}/usdt/binance/{ticker_base.lower()}usdt_perp/price-chart-live/?tab=watchlists" target="_blank">{ticker_base}USDT</a>'
        return link1
    
    elif ticker.endswith('-USD'):
        ticker_base = ticker.replace('-USD', '')
        return f'<a href="https://br.tradingview.com/chart/JKfvODlT/?symbol=BINANCE%3A{ticker_base}USDT" target="_blank">{ticker_base}-USD</a>'
    
    else:
        ticker = ticker.split("'")[1] if "'" in ticker else ticker
        ticker = ticker.replace(".SA", "")
        return f'<a href="https://br.tradingview.com/chart/JKfvODlT/?symbol=BMFBOVESPA%3A{ticker}" target="_blank">{ticker}</a>'
    

def style_dataframe(df):
    def apply_color(val, value):
        if pd.notna(val) and pd.notna(value) and val <= value:
            return f'background-color: green; color: white'
        return ''

    # Aplica a formatação verde, exceto nas colunas RSI
    for index, row in df.iterrows():
        value = row['Value']
        for col in df.columns:
            if col != 'Value' and not col.startswith('RSI'):
                df.at[index, col] = f'<span style="{apply_color(row[col], value)}">{row[col]}</span>'

    # Agora aplica o gradiente nas colunas RSI
    styled_df = df.style.map(rsi_gradient, subset=['RSI 1h', 'RSI Day', 'RSI Week']) \
                        .format(na_rep='-')

    return styled_df

def rsi_gradient(val):
    """Define a gradiente de cor para RSI baseada no valor, com intervalo de 20 a 80."""
    if pd.isna(val):
        return ''
    # Gradiente de verde (baixo) a vermelho (alto) entre 20 e 80
    if val < 20:
        return 'color: green'
    elif val > 80:
        return 'color: red'
    else:
        green = int(255 * (1 - (val - 20) / 60))
        red = int(255 * ((val - 20) / 60))
        return f'color: rgb({red}, {green}, 0)'  # Formato rgb