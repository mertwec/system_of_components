from app_comp import app    #, db
from flask import render_template, redirect, url_for, flash, request
from app_comp.models import temp_bd, Category, Pattern, Component, PCBoard, AssociatedCompPcb
from app_comp.forms import PatternAddForm, ComponentAddForm, \
                            PCBAddForm, CategoryAddForm
from app_comp.tools.forms_validation import *
from app_comp.tools.quotes import random_quote
import app_comp.tools.database_tools as dbt
import app_comp.tools.preparing_filereport_date as pfrd
from decimal import Decimal


crud = dbt.CRUDTable()

@app.route('/')
@app.route('/index')
@app.route('/creation')
def index():
    temp_bd['quote'] = random_quote()
    return render_template("index.html", title="Home", bd=temp_bd)


@app.route('/categories/<string:type_category>', methods=['get'])
def categories(type_category='menu'):
    all_cat = crud.read_table_sorted(Category, Category.name)
    category = type_category
    if category != 'menu':
        components_from_category = dbt.get_components_from_category(category, Component)
        if components_from_category:
            temp_bd['quote'] = random_quote()
            return render_template("categories.html",
                                   title='menu Categories',
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


@app.route('/creation/component', methods=['get', 'post'])
def create_component():
    form = ComponentAddForm()
    form.pattern.choices = [p[0] for p in crud.read_table_all(Pattern.name)]
    form.category.choices = [c[0] for c in crud.read_table_all(Category.name)]
    if form.validate_on_submit():
        all_data = form.data    # get all data from form
        component_date = generate_component_for_db(all_data)
        if isinstance(component_date, str):
            flash(f"{component_date}", "Warning")   # unit and category do not correspond!
        elif isinstance(component_date, dict):
            # validation
            name = (component_date["value"],
                    component_date['pattern_name'],
                    component_date['tolerance'],)
            category = component_date['category_name']
            names_db = dbt.get_components_from_category(category,
                                                        Component.value,
                                                        Component.pattern_name,
                                                        Component.tolerance,)
            if check_exist_value_in_db(name, names_db):
                flash(f'Component  "{name}" already exists', 'Warning')
            else:
                dbt.create_component(component_date)
                flash(f"component {component_date['category_name']}: {component_date['value']} is created", 'Success')
        return redirect(url_for('create_component'))

    temp_bd['quote'] = random_quote()
    return render_template('create/creation.html',
                           title='Component',
                           form=form,
                           bd=temp_bd)


@app.route("/creation/pattern", methods=['get', 'post'])
def create_pattern():
    form = PatternAddForm()
    if form.validate_on_submit():
        name = form.name.data.upper()
        names_db = (i[0] for i in crud.read_table_all(Pattern.name))
        # validations
        if check_exist_value_in_db(name, names_db):
            flash(f'Pattern "{name}" already exists', 'Warning')
        else:
            new_pattern = Pattern(name=name)
            crud.write_to_table_column(new_pattern)
            flash(f'Pattern "{name}" is created', 'Success')
        return redirect(url_for('create_pattern'))

    temp_bd['quote'] = random_quote()
    return render_template('create/creation.html',
                           title='Pattern',
                           form=form,
                           bd=temp_bd)


@app.route("/creation/category", methods=['get', 'post'])
def create_category():
    form = CategoryAddForm()
    if form.validate_on_submit():
        name = form.name.data.lower()
        refdes = form.refdes.data
        names_db = (i.name for i in crud.read_table_all(Category.name))
        # validations
        if check_exist_value_in_db(name, names_db):
            flash(f'Category "{name}" already exists', 'Warning')
        else:
            new_category = Category(name=name, refdes=refdes)
            crud.write_to_table_column(new_category)
            flash(f'Category "{name}" ({refdes}) is created', 'Success')
        return redirect(url_for('create_category'))

    temp_bd['quote'] = random_quote()
    return render_template('create/creation.html',
                           title='Category',
                           form=form,
                           bd=temp_bd)


@app.route('/creation/PCB', methods=['GET', 'POST'])
def create_pcb():
    form = PCBAddForm()
    if form.validate_on_submit():
        data = form.data
        name = data["name"].upper()
        version = data["version"]
        print(form.name)
        pcb_db = ((i.name, i.version) for i in crud.read_table_all(PCBoard))
        if check_exist_value_in_db((name, version), pcb_db):
            flash(f'Board "{name}" {version} already exists', 'Warning')

        elif request.method == "POST" and data["file_report"] and data['submit']:
            _data = request.files[form.file_report.name]     # get file
            file_name = f"{name}-{version}"      # all name loaded file "DRIXDN630YI-3.0_SiC(30kW).csv"
            file_object = _data.stream.read()    # read file

            # get only unique components from file_object(readed report_file) [pcb_name, {parameters from file_object}]
            prepared_file_object = pfrd.select_unique_component(file_object, pcb_name=file_name)
            # dict(refdes: category name)
            map_rdcateg = dbt.map_refdes_category()
            # converting a component to write to db
            pcb_components = pfrd.parsing_components(prepared_file_object[1], map_rdcateg)
            # check component on exist in db
            pcb_components_in_db = dbt.exists_components_in_db(pcb_components)

            form.name = name
            form.version = version
            form.comment = data["comment"]
            form.count_boards = data["count_boards"]
            form.file_report = _data
            print(2, _data)
            return render_template('create/create_pcb.html',
                                   prepared_rep_file=pcb_components_in_db,
                                   title='creation PCBoard',
                                   form=form,
                                   bd=temp_bd)

        elif request.method == "POST" and data['submit_create']:
            print('create')
            print(3, data)
        # else:
        #     new_pcb = PCBoard(name=name,
        #                       version=version,
        #                       count_boards=count_b)
        #     # crud.write_to_table_column(new_pcb)
        #    flash(f'PCB "{name} {version}" is created', 'Success')

        return redirect(url_for('create_pcb'))
    temp_bd['quote'] = random_quote()
    return render_template('create/create_pcb.html',
                           title='creation PCBoard',
                           form=form,
                           bd=temp_bd)
