from controller.controller_manager import ControllerManager
from view.get_user_asset_selection import get_user_asset_selection

from IPython.display import clear_output, HTML, display
import pandas as pd

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
            self.analyzed_assets.index = [self.link_tradingview(ticker) for ticker in self.analyzed_assets.index]
            styled_df = self.style_dataframe(self.analyzed_assets)
            
            # display(styled_df)
            display(HTML(styled_df.to_html(escape=False))) 

    def link_tradingview(self, ticker):
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
        
    def rsi_gradient(self, val):
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

    def style_dataframe(self, df):
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
        styled_df = df.style.map(self.rsi_gradient, subset=['RSI 1h', 'RSI Day', 'RSI Week']) \
                            .format(na_rep='-')

        return styled_df

    # def style_dataframe(self, df):
    #     """Aplica o estilo ao DataFrame somente para o RSI."""
    #     # Aplica o estilo de gradiente apenas às colunas de RSI
    #     styled_df = df.style.applymap(self.rsi_gradient, subset=['RSI 1h', 'RSI Day', 'RSI Week']) \
    #                         .format(na_rep='-')
    #     return styled_df


    
    # def style_dataframe(self, df):
    # # Funções de estilo para coloração do texto das colunas RSI e EMA
    #     def yellow_text(val):
    #         return 'color: #deda14' if val else ''
        
    #     def blue_text(val):
    #         return 'color: #0095ff' if val else ''
        
    #     def red_text(val):
    #         return 'color: #FFA07A' if val else ''
        
    #     def white_text(val):
    #         return 'color: white' if val else ''
        
    #     # Aplicando estilos ao texto das colunas RSI e EMA
    #     styled_df = df.style.map(yellow_text, subset=['RSI 1h', 'EMA 1h']) \
    #                         .map(blue_text, subset=['RSI Day', 'EMA Day']) \
    #                         .map(red_text, subset=['RSI Week', 'EMA Week']) \
    #                         .map(white_text, subset=['Value'])

    #     return styled_df








# def display_analise(analise, visualizar=''):
#     # Se visualizar não estiver vazio, filtra o DataFrame de acordo com a condição
#     if visualizar:
#         analise = analise[analise['possivel entrada?'] == visualizar]

#     # Substituir os valores no DataFrame
#     analise = analise.rename(index=lambda x: x.replace('^BVSP', 'IBOV').replace('BRL=X', 'USD/BRL'))

#     # Cria o link no índice
#     analise.index = [link_tradingview(ticker) for ticker in analise.index]

#     # Definir a ordem categórica desejada para a coluna 'Tendencia'
#     ordem_categorica = ['baixa forte', 'baixa', 'neutro', 'alta', 'alta forte']
#     analise['Tendencia'] = pd.Categorical(analise['Tendencia'], categories=ordem_categorica, ordered=True)

#     # Ordenar o DataFrame com base na ordem categórica definida
#     analise.sort_values(by='Tendencia', inplace=True)

#     # Aplicar formatação condicional a cada coluna
#     colunas = ['Tendencia', 'Longo_Prazo', 'possivel entrada?']
#     analise_colorida = analise.style.applymap(colorir, subset=colunas)

#     # Chame esta função após a exibição inicial do DataFrame formatado
#     analise_colorida = colorir_fibos(analise_colorida)

#     # Exibir DataFrame com formatação condicional
#     display(analise_colorida)


# def colorir(valor):
#     if valor in ['alta', 'alta forte','Sim']:
#         return 'color: green'
#     elif valor in ['baixa', 'baixa forte','Não']:
#         return 'color: red'
#     elif valor in ['neutro']:
#         return 'color: blue'
#     else:
#         return 'color: black'  # Manter a cor padrão para outros valores
    

# def link_tradingview(ticker):
#     # Retornar link específico para USD/BRL
#     if isinstance(ticker, tuple):
#         ticker = ticker[0]  # Extrai o ticker se for uma tupla
#     if ticker == 'USD/BRL':
#         return f'<a href="https://br.tradingview.com/chart/JKfvODlT/?symbol=FX_IDC%3AUSDBRL" target="_blank">{ticker}</a>'
#     # Retornar link específico para tickers terminados com -USD
#     elif ticker.endswith('-USD'):
#         ticker = ticker.replace('-USD', '')  # Remove '-USD' do ticker
#         return f'<a href="https://br.tradingview.com/chart/JKfvODlT/?symbol=BINANCE%3A{ticker}USDT" target="_blank">{ticker}-USD</a>'
#     # Retornar link padrão para outros ativos
#     else:
#         ticker = ticker.split("'")[1] if "'" in ticker else ticker  # Pega o ticker
#         ticker = ticker.replace(".SA", "")  # Remove '.SA' se presente
#         return f'<a href="https://br.tradingview.com/chart/JKfvODlT/?symbol=BMFBOVESPA%3A{ticker}" target="_blank">{ticker}</a>'


