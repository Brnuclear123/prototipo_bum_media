import random
import os
import requests
from flask import Flask, render_template, redirect, url_for, request, session, abort, jsonify
import mysql.connector
from jinja2 import ChoiceLoader, FileSystemLoader
from dotenv import load_dotenv
#from app import app, get_db_connection

load_dotenv
app = Flask(__name__)

# Carregar a chave da API a partir do .env
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/get_weather', methods=['GET'])
def get_weather():
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')

    if not latitude or not longitude:
        return jsonify({'error': 'Coordenadas não fornecidas'}), 400

    # URL da API de clima atual
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}&units=metric&lang=pt_br"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'error': 'Erro ao consultar a API de clima', 'details': response.json()}), 500

    # Processar a resposta da API para obter apenas a temperatura
    weather_data = response.json()
    clima = {
        'temperatura_atual': weather_data['main']['temp']
    }

    return jsonify(clima)

# Configuração do Banco de Dados
app.config['DB_HOST'] = 'localhost'
app.config['DB_USER'] = 'root'
app.config['DB_PASSWORD'] = 'TodoMundo1234'
app.config['DB_NAME'] = 'bump_media'

# Função para conectar ao banco de dados
import pymysql

def get_db_connection():
    try:
        conn = pymysql.connect(
            host=app.config['DB_HOST'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_NAME']
        )
        return conn
    except pymysql.MySQLError as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        raise


@app.route('/test_db')
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        cursor.close()
        conn.close()
        return f"Conectado ao banco de dados: {db_name[0]}"
    except Exception as e:
        return f"Erro ao conectar ao banco de dados: {e}"

app.secret_key = "sua_chave_secreta"

# Configuração para múltiplas pastas de templates
app.jinja_loader = ChoiceLoader([
    FileSystemLoader('templates')
])

# Usuários de exemplo com tipos de acesso
users = {
    "dev": {"password": "1234", "role": "developer"},
    "client_user": {"password": "1234", "role": "client"}
}

# Decorador para verificar se o usuário está logado e tem o papel correto
def login_required(role=None):
    def wrapper(f):
        def decorated_function(*args, **kwargs):
            if 'role' not in session:
                return redirect(url_for('login'))
            if role and session['role'] != role:
                abort(403)  # Proibido
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return wrapper

# Rota principal que redireciona para a visão correta
@app.route('/')
def index():
    if 'role' in session:
        if session['role'] == 'developer':
            return redirect(url_for('dev_overview'))
        elif session['role'] == 'client':
            return redirect(url_for('client_overview'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)

        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('index'))
        else:
            error = "Usuário ou senha incorretos."
            return render_template('login.html', error=error)
    
    return render_template('login.html')

# --------------------
# Rotas para Developer
# --------------------
@app.route('/index')
@login_required(role='developer')
def dev_overview():
    return render_template('index.html')

@app.route('/clients')
@login_required(role='developer')
def dev_clients():
    return render_template('clients.html')

@app.route('/system')
@login_required(role='developer')
def dev_system():
    return render_template('system.html')

@app.route('/moderation')
@login_required(role='developer')
def dev_moderation():
    return render_template('moderation.html')

@app.route('/analytics')
@login_required(role='developer')
def dev_analytics():
    return render_template('analytics.html')

@app.route('/content_ai')
@login_required(role='developer')
def dev_content_ai():
    return render_template('content_ai.html')

@app.route('/campaign')
@login_required(role='developer')
def dev_campaign():
    return render_template('campaign.html')

@app.route('/assets')
@login_required(role='developer')
def dev_assets():
    return render_template('assets.html')

@app.route('/company_profile')
@login_required(role='developer')
def dev_company_profile():
    return render_template('company_profile.html')

# Rota para processar e salvar os dados enviados pelo formulário
@app.route('/save_company_profile', methods=['POST'])
def save_company_profile():
    company_name = request.form['company_name']
    location_data = request.form['location_data']
    brand_tone = request.form['brand_tone']
    target_audience = request.form['target_audience']
    call_to_action = request.form['call_to_action']

    # Conectar ao banco de dados e inserir os dados
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO company_profiles (company_name, location_data, brand_tone, target_audience, call_to_action)
        VALUES (%s, %s, %s, %s, %s)
    """, (company_name, location_data, brand_tone, target_audience, call_to_action))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('company_profile'))
# --------------------
# Rotas para Client
# --------------------
@app.route('/client/overview')
@login_required(role='client')
def client_overview():
    return render_template('client_overview.html')

@app.route('/client/content_ai')
@login_required(role='client')
def client_content_ai():
    return render_template('client_content_ai.html')

@app.route('/client/campaign')
@login_required(role='client')
def client_campaign():
    return render_template('client_campaign.html')

@app.route('/client/assets')
@login_required(role='client')
def client_assets():
    return render_template('client_assets.html')

@app.route('/client/analytics')
@login_required(role='client')
def client_analytics():
    return render_template('client_analytics.html')

@app.route('/client/moderation')
@login_required(role='client')
def client_moderation():
    return render_template('client_moderation.html')

@app.route('/client/company_profile')
@login_required(role='client')
def client_company_profile():
    return render_template('client_company_profile.html')

# Rota de logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
