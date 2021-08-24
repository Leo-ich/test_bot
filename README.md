## Тестовый Telegram бот.

https://t.me/TzorTestBot

### Требования задания:

Бот задаёт несколько вопросов и сохраняет ответы в базу.
 * Python 3.5
 * PostgresSQL без ORM
 * Метод для выборки из базы с фильтром по всем полям

### Развёртывание:

Для запуска нужно задать переменные окружения DB_PASS, API_TOKEN, и/или настройки
 подключения к базе в файле config.py

#### Запуск на Heroku:

создаём приложение и базу данных на heroku, затем

    cd myapp
    heroku login -i
    heroku config:set API_TOKEN=xxxxxxx
    heroku git:remote -a appname
    heroku stack:set container -a appname
    git push heroku master
    
Теперь переход на WEBHOOK_HOST включит вебхук режим бота.

#### Локальная сборка docker контейнера:

    podman build -t telegram_bot:latest ./

#### Локальный запуск docker контейнера:
    
    podman run -it --rm --env-file .env -p 5000:8443 telegram_bot:latest
    
Теперь переход по адресу http://localhost:5000/ отключит вебхук режим бота.