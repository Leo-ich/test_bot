from config import Config

bind = ['{}:{}'.format(Config.WEBHOOK_LISTEN, Config.WEBHOOK_PORT)]
keyfile = getattr(Config, 'WEBHOOK_SSL_PRIV', '')
certfile = getattr(Config, 'WEBHOOK_SSL_CERT', '')



