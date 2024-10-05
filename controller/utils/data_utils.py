import json

def load_assets(file_path):
    '''Carrega a lista de ativos do arquivo JSON do PATH'''
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
