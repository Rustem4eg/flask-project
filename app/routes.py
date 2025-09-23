from flask import render_template, request, redirect, url_for
from app import app
import random

# Список случайных шуток
JOKES = [
    "Татарские шахматы — это когда конь ходит как слон, слон как ферзь, ферзь как король, а король просто сидит и говорит: «Син мине тынлаган иденме?» (Ты меня понимаешь?).",
    "Татарский способ похудения — это когда ты говоришь «кил монда» (иди сюда) холодильнику, а он отвечает «син кил монда» (ты иди сюда), и в итоге ты сам отказываешься от еды из принципа.",
    "Татарский этикет — это когда ты приходишь в гости, а хозяин говорит: «Не откажи в любезности, поешь», и ты вынужден съесть всё, потому что отказаться — значит обидеть человека, а съесть всё — значит обидеть свой желудок.",
    "Татарский секрет долголетия — это умение одновременно есть эчпочмак, пить чай из пиалы и рассказывать истории про предков, при этом не проливая ни капли и не роняя ни кусочка.",
    "Татарская мудрость: если ты не можешь выбрать между чаем и бульоном — бери оба, потому что настоящий татарин должен быть готов ко всему, даже к тому, что гости придут раньше, чем ты успеешь всё приготовить."
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