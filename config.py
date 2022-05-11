import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'BIg_secret-key1223_sosi_hyi_i_ne_psixyi_485476867'

    # DATABASE_URL -- переменная среды в которой хранится ссылка на БД (postgresql)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        'sqlite:///' + os.path.join(basedir, 'database_components.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # сигнализирует приложению каждый раз, когда в базе данных должно быть внесено изменение.(прожорлив на ресурсы)
