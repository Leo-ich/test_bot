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

    
    # генерируем самоподписанный сертификат и приватный ключ
    
    openssl req -x509 -days 3650 -out webhook_cert.crt -keyout webhook_pkey.key \
    -newkey rsa:2048 -nodes -sha256 \
    -subj '/CN=tzortestbot.herokuapp.com' -extensions EXT -config <( \
    printf "[dn]\nCN=tzortestbot.herokuapp.com\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:tzortestbot.herokuapp.com\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
    
    # В "Common Name (eg, your name or your server's hostname)"
    # следует указать IP адрес сервера или доменное имя сервера

Сборка docker контейнера:

    podman build -t telegram_bot:latest ./

Запуск docker контейнера:
    
    podman run -d --rm --env-file .env -p 5000:8443 telegram_bot:latest