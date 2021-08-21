
class Config(object):

    # set bot
    # API_TOKEN = ''
    # WEBHOOK_HOST = 'https://your_heroku_project.com/'
    WEBHOOK_PORT = 8443  # 443, 80, 88, 8443
    WEBHOOK_LISTEN = '0.0.0.0'
    WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # Path to the ssl certificate
    WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # Path to the ssl private key

    # set data base
    DB_NAME = 'bot_db'
    DB_USER_NAME = 'postgres'
    DB_PASS = ''
    DB_HOST = '192.168.1.3'
    DB_PORT = 5432
