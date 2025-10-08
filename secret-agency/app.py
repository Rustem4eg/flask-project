# app.py
# Секретное агентство: управление досье агентов
# Автор: разведчик-разработчик

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель агента — каждое досье это запись в таблице
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codename = db.Column(db.String(100), nullable=False, unique=True)
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    clearance_level = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Agent {self.codename}>'

# Генератор кодовых имён — на случай если шеф не придумал
def make_codename():
    parts1 = ['Серый', 'Неистовый', 'Тихоня', 'Черный', 'Красный', 'Сыкливый', 'Крепкий']
    parts2 = ['Волк', 'Ворон', 'Стрекозел', 'Грин', 'Сайгак', 'Вризрак', 'Куркуль']
    return f"{random.choice(parts1)} {random.choice(parts2)}"

# Уровни допуска — строго по регламенту
CLEARANCE_OPTIONS = ["Секретно", "Совершенно секретно", "Особой важности"]

# Создаём таблицы при старте (если их ещё нет)
with app.app_context():
    db.create_all()

# Главная — список всех агентов
@app.route('/')
def index():
    agents = Agent.query.all()
    return render_template('agents.html', agents=agents)

# Добавление нового агента
@app.route('/add', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        name = request.form.get('codename').strip()
        if not name:
            name = make_codename()
        phone = request.form['contact_number']
        mail = request.form['email']
        level = request.form['clearance_level']

        agent = Agent(
            codename=name,
            contact_number=phone,
            email=mail,
            clearance_level=level
        )
        db.session.add(agent)
        db.session.commit()
        return redirect(url_for('index'))

    # При GET-запросе показываем форму + подсказку по имени
    suggested = make_codename()
    return render_template('add_agent.html', suggested_name=suggested, levels=CLEARANCE_OPTIONS)

# Просмотр досье
@app.route('/agent/<int:id>')
def view_agent(id):
    agent = Agent.query.get_or_404(id)
    return render_template('view_agent.html', agent=agent)

# Редактирование
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_agent(id):
    agent = Agent.query.get_or_404(id)
    if request.method == 'POST':
        agent.codename = request.form['codename']
        agent.contact_number = request.form['contact_number']
        agent.email = request.form['email']
        agent.clearance_level = request.form['clearance_level']
        db.session.commit()
        return redirect(url_for('view_agent', id=id))

    return render_template('edit_agent.html', agent=agent, levels=CLEARANCE_OPTIONS)

# Удаление
@app.route('/delete/<int:id>')
def delete_agent(id):
    agent = Agent.query.get_or_404(id)
    db.session.delete(agent)
    db.session.commit()
    return redirect(url_for('index'))

# Фильтр по уровню допуска
@app.route('/filter/<level>')
def filter_by_level(level):
    if level not in CLEARANCE_OPTIONS:
        return redirect(url_for('index'))
    agents = Agent.query.filter_by(clearance_level=level).all()
    return render_template('agents.html', agents=agents, current_filter=level)

# Экстренный вызов — просто показывает уведомление
@app.route('/emergency/<int:id>')
def emergency_call(id):
    agent = Agent.query.get_or_404(id)
    msg = f"🚨 Экстренное оповещение отправлено агенту {agent.codename} ({agent.email})"
    agents = Agent.query.all()
    return render_template('agents.html', agents=agents, alert=msg)

# Запуск
if __name__ == '__main__':
    app.run(debug=True)