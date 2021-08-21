from config import Config

bind = ['{}:{}'.format(Config.WEBHOOK_LISTEN, Config.WEBHOOK_PORT)]
keyfile = Config.WEBHOOK_SSL_PRIV
certfile = Config.WEBHOOK_SSL_CERT


