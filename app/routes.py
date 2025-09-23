from flask import render_template, request, redirect, url_for
from app import app
import random

# Список случайных шуток
JOKES = [
    "Почему программисты не ходят в лес? Боятся веток!",
    "Какой язык программирования самый грустный? — JavaScript, потому что все его проблемы асинхронны.",
    "Зачем программисту мыло? Чтобы отмыть баги!",
    "Если бы Java была человеком — она бы сказала: 'Я не умру, я просто стану сборщиком мусора.'",
    "Программист заходит в бар... 0x7F454C46 — это уже не шутка, это ELF-файл."
]

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        color = request.form.get("color", "#ffffff")
        profession = request.form.get("profession")
        hobbies = request.form.getlist("hobbies")  # чекбоксы
        level = request.form.get("level")

        # Выбираем случайную шутку
        joke = random.choice(JOKES)

        return render_template(
            "result.html",
            name=name,
            email=email,
            color=color,
            profession=profession,
            hobbies=hobbies,
            level=level,
            joke=joke
        )
    else:
        return redirect(url_for("form"))