from app_comp import app, db
from flask import render_template
from app_comp.models import temp_bd, Category


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home", bd=temp_bd)


@app.route('/categories')
def categories():
    all_cat = db.session.query(Category).all()
    return render_template("categories.html",
                           title='Categories',
                           all_categories=all_cat,
                           bd=temp_bd)
