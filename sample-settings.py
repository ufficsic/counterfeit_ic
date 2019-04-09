import os

SECRET_KEY = os.urandom(24)
DEBUG=True
DB_USERNAME = 'user_name'
DB_PASSWORD = 'passwword'
DB_NAME = 'db_name'
DB_PORT = 0000
DB_HOST = 'db_ip'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%d/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = True