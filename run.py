# запуск приложения
from app import app

if __name__ == '__main__':
    # запускаем в debug-режиме, чтобы видеть ошибки
    app.run(debug=True)