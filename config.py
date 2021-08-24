from os import environ, path
from urllib.parse import urlparse

from dotenv import load_dotenv

# set environment variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class BaseConfig(object):

    # set bot
    API_TOKEN = '' or environ['API_TOKEN']
    WEBHOOK_HOST = ''
    WEBHOOK_PORT = environ.get('PORT', 8443)  # 443, 80, 88, 8443
    WEBHOOK_LISTEN = '127.0.0.1'
    WEBHOOK_SSL_CERT = 'webhook_cert.crt'  # Path to the ssl certificate
    WEBHOOK_SSL_PRIV = 'webhook_pkey.key'  # Path to the ssl private key

    # set data base
    DB_NAME = 'bot_db'
    DB_USER_NAME = 'postgres'
    DB_PASS = '' or environ.get('DB_PASS', None)
    DB_HOST = 'localhost'
    DB_PORT = 5432


class DevelopmentConfig(BaseConfig):

    # set bot
    WEBHOOK_SSL_CERT = ''
    WEBHOOK_SSL_PRIV = ''

    # set data base
    DB_HOST = '192.168.1.3'


class HerokuProdConfig(BaseConfig):

    # set bot
    WEBHOOK_HOST = 'https://tzortestbot.herokuapp.com/'
    WEBHOOK_LISTEN = '0.0.0.0'
    WEBHOOK_SSL_CERT = ''
    WEBHOOK_SSL_PRIV = ''

    # set data base
    DATABASE_URL = environ.get('DATABASE_URL', None)
    result = urlparse(DATABASE_URL)
    DB_NAME = result.path[1:]
    DB_USER_NAME = result.username
    DB_PASS = result.password
    DB_HOST = result.hostname
    DB_PORT = result.port


DYNO = environ.get('DYNO', '')  # it is Heroku dyno runtimes
if DYNO:
    Config = HerokuProdConfig
else:
    Config = DevelopmentConfig
