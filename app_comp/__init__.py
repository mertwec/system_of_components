from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db,)

# since in 'views' import app because import here
from app_comp import models, views
from app_comp.models import Component, Category, Pattern, PCBoard, AssociatedCompPcb


@app.shell_context_processor
def make_shell_context():
    """for default import in "flask shell"
    """
    return {'db': db,
            'Component': Component,
            'Category': Category,
            'Pattern': Pattern,
            'PCBoard': PCBoard,
            'AssociatedCompPcb': AssociatedCompPcb,
            }
