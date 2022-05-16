import os


basedir = os.path.abspath(os.path.dirname(__file__))


class ConfigTest(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or '52a79a4394be4fd68b9dd012680d6cb8'

    # DATABASE_URL -- переменная среды в которой хранится ссылка на БД (postgresql)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        'sqlite:///' + os.path.join(basedir, 'database_components.db')

    # сигнализирует приложению каждый раз, когда в базе данных
    # должно быть внесено изменение.(прожорлив на ресурсы)
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '52a79a4394be4fd68b9dd012680d6cb8'
    SQLALCHEMY_DATABASE_URI = "postgresql://torsion:torsionplus@localhost:5432/componentsdb"
                                #"postgresql://<username>:<password>@<server>:5432/<db_name>"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
