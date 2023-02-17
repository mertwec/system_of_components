import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config, ConfigTest


sep = os.sep
abs_path = os.path.abspath(rf".{sep}")   # D:\PyProgect\system_of_components
path_to_json = abs_path + rf"{sep}app_comp{sep}static{sep}quotes.json"

app = Flask(__name__)
app.config.from_object(ConfigTest)     # sqlite
# app.config.from_object(Config)       # postgres

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# since in 'views' import app because import here
from app_comp import models, views
from app_comp.models import Component, Category, Pattern, PCBoard, AssociatedCompPcb


@app.shell_context_processor
def make_shell_context():
    """for default import in "flask shell"
    """
    return {'db': db,
            'app': app,
            'Component': Component,
            'Category': Category,
            'Pattern': Pattern,
            'PCBoard': PCBoard,
            'AssociatedCompPcb': AssociatedCompPcb,
            }
