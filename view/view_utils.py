import pandas as pd
from IPython.display import clear_output

def get_global_asset_selection():
    print("Select the group of assets for analysis:")
    print("(1) Brazilian Stocks")
    print("(2) Brazilian REITs")
    print("(3) Cryptocurrencies")
    print("(4) Cancel")
    asset_choice = input("Enter your choice (1, 2, 3, or 4): ")

    while asset_choice not in ['1', '2', '3', '4']:
        asset_choice = input("Invalid choice. Please select one of the available options (1, 2, 3, or 4): ")

    clear_output(wait=True) 
    return asset_choice


def link_tradingview(ticker):
    # Retornar link específico para USD/BRL
    if isinstance(ticker, tuple):
        ticker = ticker[0]  # Extrai o ticker se for uma tupla
    if ticker == 'USD/BRL':
        return f'<a href="https://br.tradingview.com/chart/JKfvODlT/?symbol=FX_IDC%3AUSDBRL" target="_blank">{ticker}</a>'
    # Retornar link específico para tickers terminados com -USD
    elif ticker.endswith('-USD'):
        ticker = ticker.replace('-USD', '')  # Remove '-USD' do ticker
        return f'<a href="https://br.tradingview.com/chart/JKfvODlT/?symbol=BINANCE%3A{ticker}USDT" target="_blank">{ticker}-USD</a>'
    # Retornar link padrão para outros ativos
    else:
        ticker = ticker.split("'")[1] if "'" in ticker else ticker  # Pega o ticker
        ticker = ticker.replace(".SA", "")  # Remove '.SA' se presente
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