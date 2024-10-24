from flask import Flask, render_template, request, jsonify
from view.view_manager import ViewManager

import requests

app = Flask(__name__)
view_manager = ViewManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blank')
def blank():
    return render_template('blank.html')

@app.route('/404')
def page404():
    return render_template('404.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.route('/global-assets')
def global_assets():
    return render_template('global-assets.html')

@app.route('/personal-assets')
def personal_assets():
    return render_template('personal-assets.html')

@app.route('/register-transaction')
def register_transaction():
    return render_template('register-transaction.html')

@app.route('/charts-index')
def charts_index():
    return render_template('charts-index.html')

@app.route('/charts-crypto')
def charts_crypto():
    return render_template('charts-crypto.html')

@app.route('/transaction-review')
def transaction_review():
    return render_template('transaction-review.html')
    
@app.route('/portfolio-review')
def portfolio_review():
    return render_template('portfolio-review.html')

@app.route('/analyze-my-assets')
def analyze_my_assets():
    return render_template('analyze-my-assets.html')

@app.route('/portfolio-pie-chart')
def portfolio_chart():
    return jsonify(view_manager.get_portfolio_chart_data())

@app.route('/api/insert-transaction', methods = ['POST'])
def insert_transaction():
    data = request.json
    result =  {"message":     
        view_manager.insert_db_transaction(
            corretora=data['corretora'],
            data=data['data'], 
            tipo=data['tipo'], 
            ticker=data['ticker'], 
            transacao=data['transacao'], 
            cotas=data['cotas'], 
            preco_unitario=data['preco_unitario'], 
            taxa=data['taxa']
        )}

    return jsonify(result)

@app.route('/api/analyze-global-assets', methods=['POST'])
def analyze_global_assets():
    data = request.json
    
    result = view_manager.analyze_global_assets(data.get("selected"))

    result = result.to_json(orient='records')

    if result:
        return result
    else:
        return jsonify({'error': 'No assets analyzed.'}), 404


@app.route('/api/analyze-personal-assets', methods=['POST'])
def analyze_personal_assets():
    data = request.json

    result = view_manager.analyze_personal_assets(data.get('selected'), data.get('assetType')).to_json(orient='records')
    
    if result:
        return result
    else:
        return jsonify({'error': 'No assets analyzed.'}), 404
    
@app.route('/ibovespa', methods=['GET'])
def get_ibovespa_data():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EBVSP?range=1d&interval=1d"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)  # Retorna os dados para o frontend

    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"Erro HTTP: {http_err}"}), 400
    except Exception as err:
        return jsonify({"error": f"Ocorreu um erro: {err}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
