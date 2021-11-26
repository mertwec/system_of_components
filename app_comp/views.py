from app_comp import app, db
from flask import render_template, redirect, url_for, flash, request
from app_comp.models import temp_bd, Category, Pattern, Component
from app_comp.forms import PatternAddForm, ComponentAddForm
from app_comp.tools.forms_validation import *
from app_comp.tools.database_tools import write_component_to_table, \
                                            write_column_to_table, \
                                            get_components_from_category
from app_comp.tools.quotes import random_quote
from decimal import Decimal


@app.route('/')
@app.route('/index')
def index():
    temp_bd['quote'] = random_quote()
    return render_template("index.html", title="Home", bd=temp_bd)


@app.route('/categories/<string:type_category>', methods=['get'])
def categories(type_category='menu'):
    all_cat = db.session.query(Category).order_by(Category.name).all()
    category = type_category
    if category != 'menu':
        components_from_category = get_components_from_category(db, category, Component)
        if components_from_category:
            temp_bd['quote'] = random_quote()
            return render_template("categories.html",
                                   title='Categories',
                                   all_categories=all_cat,
                                   components_of_category=components_from_category,
                                   bd=temp_bd, )
        else:
            return redirect(url_for("categories", type_category='menu'))
    else:
        temp_bd['quote'] = random_quote()
        return render_template("categories.html",
                               title='Categories',
                               all_categories=all_cat,
                               bd=temp_bd,)


@app.route('/creation', methods=['get', 'post'])
def create_component():
    form = ComponentAddForm()
    if form.validate_on_submit():
        all_data = form.data    # get all data from form
        print('form date:', all_data)
        component_date = generate_component_for_db(all_data)
        if isinstance(component_date, str):
            flash(f"{component_date}", "Warning")
        elif isinstance(component_date, dict):
            # validation
            name = (component_date["value"], component_date['pattern_name'])
            category = component_date['category_name']
            names_db = get_components_from_category(db, category,
                                                    Component.value,
                                                    Component.pattern_name)
            if check_exist_value_in_db(name, names_db):
                flash(f'Component  "{name}" already exists', 'Warning')
            else:
                write_component_to_table(db, component_date)
                flash(f"component {component_date['category_name']}: {component_date['value']} is created", 'Success')
        return redirect(url_for('create_component'))
    temp_bd['quote'] = random_quote()
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
            new_pattern = Pattern(name=name)
            write_column_to_table(db, new_pattern)
            flash(f'Pattern "{name}" is created', 'Success')
        return redirect(url_for('create_pattern_component'))
    temp_bd['quote'] = random_quote()
    return render_template('create_component/create_pattern.html',
                           title='creation pattern',
                           form=form,
                           bd=temp_bd)


@app.route('/test/<ig>')
def test(ig):
    print(ig)
    temp_bd['quote'] = random_quote()
    return render_template("test_pass.html", ig=ig, bd=temp_bd)
