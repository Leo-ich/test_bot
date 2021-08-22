from os import environ, path
from dotenv import load_dotenv

# set environment variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):

    # set bot
    API_TOKEN = '' or environ['API_TOKEN']
    WEBHOOK_HOST = 'https://tzortestbot.herokuapp.com/'
    WEBHOOK_PORT = environ.get('PORT', 8443)  # 443, 80, 88, 8443
    WEBHOOK_LISTEN = '0.0.0.0'
    WEBHOOK_SSL_CERT = 'webhook_cert.crt'  # Path to the ssl certificate
    WEBHOOK_SSL_PRIV = 'webhook_pkey.key'  # Path to the ssl private key

    # set data base
    DB_NAME = 'bot_db'
    DB_USER_NAME = 'postgres'
    DB_PASS = '' or environ['DB_PASS']
    DB_HOST = '192.168.1.3'
    DB_PORT = 5432
