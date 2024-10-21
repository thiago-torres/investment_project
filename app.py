from flask import Flask, render_template, request, jsonify
from view.view_manager import ViewManager

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

@app.route('/global-assets')
def global_assets():
    return render_template('global-assets.html')

@app.route('/personal-assets')
def personal_assets():
    return render_template('personal-assets.html')

@app.route('/register-transaction')
def register_transaction():
    return render_template('register-transaction.html')
    
@app.route('/chart-data')
def chart_data():
    data = view_manager.get_chart_data()    
    return jsonify(data)

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
    selected = data
    result = view_manager.analyze_global_assets(selected)

    result = result.to_json(orient='records')

    print(result)

    if result:
        return result
    else:
        return jsonify({'error': 'No assets analyzed.'}), 404


@app.route('/api/analyze-personal-assets', methods=['POST'])
def analyze_personal_assets():
    data = request.json
    selected = data.get('selected')
    asset_type = data.get('assetType')
    other_asset = data.get('otherAsset')

    if asset_type == 'outros':
        asset_type = other_asset

    result = view_manager.analyze_personal_assets(selected, asset_type)
    
    if result:
        return result
    else:
        return jsonify({'error': 'No assets analyzed.'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
