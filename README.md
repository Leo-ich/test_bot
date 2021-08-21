### Тестовый Telegram бот.
Бот задаёт несколько вопросов и сохраняет ответы в базу.
https://t.me/TzorTestBot

Требования:
 * Python 3.5
 * PostgresSQL без ORM
 * Метод для выборки из базы с фильтром по всем полям

Для запуска нужны переменные окружения DB_PASS, API_TOKEN, FLASK_APP и настройки
 подключения к базе в файле config.py
 
Для работы через webhook создадим самоподписанный сертификат:

    # генерируем приватный ключ
    openssl genrsa -out webhook_pkey.pem 2048
    
    # генерируем самоподписанный сертификат
    openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
    # В "Common Name (eg, your name or your server's hostname)"
    # следует указать IP адрес сервера или доменное имя сервера

Сборка docker контейнера:

    podman build -t telegram_bot:latest ./

Запуск docker контейнера:
    
    podman run -d --rm -e API_TOKEN=  -e DB_PASS= -p 5000:8443 telegram_bot:latest