import requests
import time

class MercadoBitcoinPublicData:
    def __init__(self):
        # Rate Limit: 1 requests/sec
        self.url = 'https://api.mercadobitcoin.net/api/v4'

    def get_fees_from_asset(self, asset, network=None):
        '''Retrieve fees for an asset, with optional network specification (e.g., ethereum)'''

        endpoint = f'{self.url}/{asset}/fees'
        params = {}
        if network:
            params['network'] = network

        try:
            response = requests.get(endpoint,params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Request failed with status code: {response.status_code}')

        except Exception as e:
            print(f'An error occurred: {e}')
            return None
    
    def get_orderbook(self, symbol, limit=None):
        '''Retrieve order book for a symbol, with optional limit (max 1000)'''

        endpoint = f'{self.url}/{symbol}/orderbook'
        params = {}
        if limit:
            params['limit'] = limit
        
        try:
            response = requests.get(endpoint,params=params)
            if response.status_code == 200:
                return response.json()            
            else:
                print (f'Request failed with status code: {response.status_code}')
                
        except Exception as e:
            print(f'An error occurred: {e}')
            return None

    def get_list_trades(self, symbol, tid=None, since=None, from_timestamp=None, to_timestamp=None, limit=None):
        '''Retrieve trades with optional filters for trade ID, timestamp range, and result limit'''

        endpoint = f'{self.url}/{symbol}/trades'
        params = {}
        if tid:
            params['tid'] = tid
        if since:
            params['since'] = since
        if from_timestamp and to_timestamp:
            params['from'] = from_timestamp
            params['to'] = to_timestamp
        if limit:
            params['limit'] = limit
        
        try:
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Request failed with status code: {response.status_code}')
                return None
        except Exception as e:
            print(f'An error occurred: {e}')
            return None
    
    def get_candles(self, symbol, resolution, start, stop = None, countback=None):
        ''' Retrieve historical candle data for a symbol, with optional countback
            symbol (e.g. BTC-BRL), resolution (1m, 15m, 1h, 3h, 1d, 1w, 1M), to = Unix timestamp
        '''       

        if stop is None:
            stop = int(time.time())
        print(stop)

        endpoint = f'{self.url}/candles'
        params = {'symbol':symbol, 'resolution':resolution, 'to':stop, 'from':start}
        if countback:
            params['countback'] = countback
        
        try:
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Request failed with status code: {response.status_code}')
                return None
        except Exception as e:
            print(f'An error occurred: {e}')
            return None
    
    def get_symbols(self, symbols=None):
        '''
        Retrieve a list of all instruments. Pass a comma-separated string of symbols 
        (e.g. BTC-BRL,LTC-BRL) to filter the results, or pass None to get all symbols.
        '''

        endpoint = f'{self.url}/symbols'
        params={}
        if symbols:
            params['symbols'] = symbols

        try:
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Request failed with status code: {response.status_code}')
                return None
        except Exception as e:
            print(f'An error occurred: {e}')
            return None

    def get_tickers(self, symbols):
        '''
        Retrieve current prices for the given symbols. 
        Symbols should be a comma-separated string (e.g., BTC-BRL,LTC-BRL).
        '''
        endpoint = f'{self.url}/tickers'
        params = {'symbols': symbols}

        try:
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Request failed with status code: {response.status_code}')
                return None
        except Exception as e:
            print(f'An error occurred: {e}')
            return None
        
    def get_networks_from_asset(self, asset):
        '''
        Retrieve networks available for withdrawal for the specified asset.
        Asset should be in BASE format (e.g., BTC).
        '''
        endpoint = f'{self.url}/{asset}/networks'

        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Request failed with status code: {response.status_code}')
                return None
        except Exception as e:
            print(f'An error occurred: {e}')
            return None