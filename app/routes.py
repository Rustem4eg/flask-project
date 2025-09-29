from flask import render_template, request, flash, redirect, url_for
from app import app
import re

# главная страница
@app.route('/')
def index():
    return render_template('index.html')

#страница о нас
@app.route('/about')
def about():
    return render_template('about.html')

# контакты — и GET, и POST
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        # если ошибки
        has_error = False

        # проверка имени
        if not name:
            flash('Пожалуйста, введите имя.', 'error')
            has_error = True

        # проверка email)
        if not email:
            flash('Email обязателен.', 'error')
            has_error = True
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Некорректный формат email.', 'error')
            has_error = True

        # проверка сообщения
        if not message:
            flash('Сообщение не может быть пустым.', 'error')
            has_error = True

        if not has_error:
            # успешная отправка
            flash('Спасибо! Ваше сообщение отправлено.', 'success')
            return redirect(url_for('contact'))  # перенаправляем, чтобы избежать повторной отправки

    # если GET или были ошибки — показываем форму
    return render_template('contact.html')