from app_comp import app, db
from flask import render_template, redirect, url_for, flash
from app_comp.models import temp_bd, Category, Pattern
from app_comp.forms import PatternAddForm, ComponentAddForm


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


@app.route("/creation", methods=['get', 'post'])
def create_component():
    form = PatternAddForm()
    if form.validate_on_submit():
        name = form.name.data
        db_names = db.session.query(Pattern.name).all()
        print(type(name), db_names)
        if (name,) in db_names:
            flash(f'Pattern "{name}" already exists', 'warning')
        else:
            # db.session.add(Pattern(name=name))
            # db.session.commit()
            print(f'pattern add "{name}"')
            flash(f'Pattern "{name}" is created', 'success')
        return redirect(url_for('create_component'))
    return render_template('create_component.html', title='creation', form=form, bd=temp_bd)


