from flask import Flask, render_template, request
import yfinance as yf
import plotly.graph_objects as go
from plotly.offline import plot
import pandas as pd

app = Flask(__name__)

# -------------------- PAGINE SITO PERSONALE --------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Qui potresti gestire i dati del modulo di contatto
        # es. invio email o salvataggio in file/database
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # (per ora non facciamo nulla con questi dati)
    return render_template('contact.html')

# -------------------- DASHBOARD --------------------

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard_index():
    plot_div = None
    error = None

    if request.method == 'POST':
        symbol = request.form.get('symbol')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(start=start_date, end=end_date)
            if hist.empty:
                error = "Nessun dato trovato. Verifica il simbolo."
            else:
                df = hist.reset_index()

                fig = go.Figure(data=[go.Candlestick(
                    x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close']
                )])

                fig.update_layout(title=f'Grafico a Candele per {symbol}',
                                  xaxis_title='Data',
                                  yaxis_title='Prezzo')

                plot_div = plot(fig, output_type='div')

        except Exception as e:
            error = f"Errore nel recupero dati: {str(e)}"

    return render_template('index.html', plot_div=plot_div, error=error)

@app.route('/dashboard/results')
def dashboard_results():
    return render_template('results.html')

@app.route('/dashboard/ui')
def dashboard_ui():
    return render_template('UI.html')

# -------------------- AVVIO SERVER --------------------

if __name__ == '__main__':
    app.run(debug=True)
