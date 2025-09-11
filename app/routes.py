from flask import Flask

app = Flask(__name__)

# Задание 1: Простые маршруты
@app.route('/hello')
def hello():
    return "Hello, world!"

@app.route('/info')
def info():
    return "This is an informational page."

# Задание 2: Динамические маршруты - сумма чисел
@app.route('/calc/<int:num1>/<int:num2>')
def calc(num1, num2):
    return f"The sum of {num1} and {num2} is {num1 + num2}."

# Обработка ошибок для нечисловых значений
@app.route('/calc/<path:invalid_path>')
def calc_error(invalid_path):
    return "Error: Please provide two integer numbers. Example: /calc/3/5"

# Задание 3: Переворот текста
@app.route('/reverse/<string:text>')
def reverse(text):
    if len(text) == 0:
        return "Error: Text must contain at least one character."
    return text[::-1]

# Задание 4: Приветствие с возрастом
@app.route('/user/<string:name>/<int:age>')
def user(name, age):
    if age < 0:
        return "Error: Age cannot be negative."
    if age > 150:
        return "Error: Please provide a realistic age."
    return f"Hello, {name}. You are {age} years old."

# Обработка ошибок для некорректного возраста
@app.route('/user/<string:name>/<path:invalid_age>')
def user_age_error(name, invalid_age):
    return f"Error: Age must be a positive integer number."

if __name__ == "__main__":
    app.run(debug=True)