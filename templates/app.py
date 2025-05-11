from flask import Flask, render_template, request, jsonify
import pandas_datareader as web
import datetime

app = Flask(__name__)

def get_historical_data(symbol, start_date, end_date):
    """
    Recupera i dati storici per un dato simbolo azionario.
    Utilizza Yahoo Finance come fonte dati tramite pandas-datareader.
    """
    try:
        df = web.DataReader(symbol, 'yahoo', start_date, end_date)
        return df.to_json(orient='records')
    except Exception as e:
        print(f"Errore nel recupero dei dati per {symbol}: {e}")
        return jsonify({'error': f'Impossibile recuperare i dati per {symbol}'}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    data = request.get_json()
    symbol = data.get('symbol')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')

    if not all([symbol, start_date_str, end_date_str]):
        return jsonify({'error': 'Parametri mancanti'}), 400

    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Formato data non valido (YYYY-MM-DD)'}), 400

    historical_data = get_historical_data(symbol, start_date, end_date)
    return historical_data

if __name__ == '__main__':
    app.run(debug=True)