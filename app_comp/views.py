from app_comp import app
from flask import render_template
from app_comp.models import temp_bd


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home", bd=temp_bd)
