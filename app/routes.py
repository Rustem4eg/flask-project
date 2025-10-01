from flask import render_template, request, flash, redirect, url_for
from app import app
import re
from datetime import datetime


@app.route('/')
def index():
    # Задание 1: передаём текущее время
    current_time = datetime.now()
    return render_template('index.html', current_time=current_time)


@app.route('/about')
def about():
    # Задание 2: список команды как список словарей
    team_members = [
        {'name': 'Алсу', 'role': 'Разработчик'},
        {'name': 'Марат', 'role': 'Дизайнер'},
        {'name': 'Рустем', 'role': 'Самый главный'}
    ]
    return render_template('about.html', team=team_members)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # Задание 3: вложенный словарь с информацией о менеджере и адресе
    manager_info = {
        'name': 'Эльвира Галимова',
        'position': 'Руководитель отдела поддержки',
        'address': {
            'street': 'ул. Шашина, д. 84',
            'city': 'Лениногорск',
            'zip': '423250'
        }
    }

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        has_error = False

        # Валидация имени
        if not name:
            flash('Пожалуйста, введите имя.', 'error')
            has_error = True

        # Валидация email
        if not email:
            flash('Email обязателен.', 'error')
            has_error = True
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Некорректный формат email.', 'error')
            has_error = True

        # Валидация сообщения
        if not message:
            flash('Сообщение не может быть пустым.', 'error')
            has_error = True

        if not has_error:
            flash('Ваше сообщение отправлено.', 'success')
            return redirect(url_for('contact'))

    # Передаём данные менеджера в шаблон
    return render_template('contact.html', manager=manager_info)