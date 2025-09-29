from flask import Flask

# создаём приложение
app = Flask(__name__)
app.secret_key = 'super-secret-key-for-flask'  # нужно для flash-сообщений

# импортируем маршруты
from app import routes