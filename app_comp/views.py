from app_comp import app, db
from flask import render_template, redirect, url_for, flash
from app_comp.models import temp_bd, Category, Pattern
from app_comp.forms import PatternAddForm, ComponentAddForm
from app_comp.tools.forms_validation import *
from app_comp.tools.database_tools import write_component_to_table, \
                                            write_pattern_to_table
from decimal import Decimal


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home", bd=temp_bd)


@app.route('/categories')
def categories():
    all_cat = db.session.query(Category).order_by(Category.name).all()
    return render_template("categories.html",
                           title='Categories',
                           all_categories=all_cat,
                           bd=temp_bd)


@app.route('/creation', methods=['get', 'post'])
def create_component():
    form = ComponentAddForm()
    if form.validate_on_submit():
        all_data = form.data
        component_date = check_component_for_db(all_data)
        if isinstance(component_date, str):
            flash(f"{component_date}", "Warning")
        elif isinstance(component_date, dict):
            write_component_to_table(db, component_date)
            flash(f"component {component_date['category_name']}: {component_date['value']} is created", 'Success')
        return redirect(url_for('create_component'))
    return render_template('create_component/create_component.html',
                           title='creation',
                           form=form,
                           bd=temp_bd)


@app.route("/creation/pattern", methods=['get', 'post'])
def create_pattern_component():
    form = PatternAddForm()
    if form.validate_on_submit():
        name = form.name.data.upper()
        names_db = [i[0] for i in db.session.query(Pattern.name).all()]
        # validations
        if check_exist_value_in_db(name, names_db):
            flash(f'Pattern "{name}" already exists', 'Warning')
        else:
            write_pattern_to_table(db, name)
            flash(f'Pattern "{name}" is created', 'Success')
        return redirect(url_for('create_pattern_component'))
    return render_template('create_component/create_pattern.html',
                           title='creation pattern',
                           form=form,
                           bd=temp_bd)
