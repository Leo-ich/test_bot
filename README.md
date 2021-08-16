### Тестовый Telegram бот.
Бот задаёт несколько вопросов и сохраняет ответы в базу.
https://t.me/TzorTestBot

Требования:
 * Python 3.5
 * PostgresSQL без ORM
 * Метод для выборки из базы с фильтром по всем полям

Для запуска нужны переменные окружения DB_PASS, API_TOKEN, FLASK_APP и настройки
 подключения к базе в файле config.py

Запуск бота:

    python -m tg_bot.py

Запуск API к базе:
    
    python -m flask run