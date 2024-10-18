from flask import Flask, render_template, request, jsonify
from view.view_manager import ViewManager

app = Flask(__name__)
view_manager = ViewManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buttons')
def buttons():
    return render_template('buttons.html')

@app.route('/cards')
def cards():
    return render_template('cards.html')

@app.route('/blank')
def blank():
    return render_template('blank.html')

@app.route('/404')
def page404():
    return render_template('404.html')
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
