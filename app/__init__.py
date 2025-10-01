from flask import Flask

# Создаём Flask-приложение
app = Flask(__name__)
app.secret_key = 'my-secret-key-for-flask-app'  # нужен для flash-сообщений

# Импортируем маршруты
from app import routes