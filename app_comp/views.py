from app_comp import app    #, db
from flask import render_template, redirect, url_for, flash, request
from app_comp.models import temp_bd, Category, Pattern, Component, \
                                    PCBoard, AssociatedCompPcb
from app_comp.forms import PatternAddForm, ComponentAddForm, \
                            PCBAddForm, CategoryAddForm, SearchForm

#from app_comp.tools.forms_validation import *

from app_comp.tools.quotes import random_quote
import app_comp.tools.database_tools as dbt
import app_comp.tools.preparing_filereport_date as pfrd
from decimal import Decimal
import pprint


crud = dbt.CRUDTable()


@app.route('/',  methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form_search = SearchForm()
    if form_search.validate_on_submit():
        search_value = form_search.value.data
        return redirect(url_for("search_component", value_for_search=search_value))
    temp_bd['quote'] = random_quote()
    return render_template("index.html", title="Home",
                           form_search=form_search,
                           bd=temp_bd)


# todo search function
@app.route('/search/<string:value_for_search>', methods=['GET'])
def search_component(value_for_search='component'):
    print('search:', value_for_search)
    temp_bd['quote'] = random_quote()
    return render_template('search/search.html',
                           title='search element',
                           search_value=value_for_search,
                           bd=temp_bd)


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
        #dbt.create_component(all_data)
        flash(f"component {all_data['category']}: {all_data['value']} is created", 'Success')
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
        new_pattern = Pattern(name=form.name.data.upper())
        crud.write_to_table_column(new_pattern)
        flash(f'Pattern "{new_pattern}" is created', 'Success')
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
        refdes = form.refdes.data.upper()
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
        if request.method == "POST" and data["file_report"] and data['submit']:
            _data = request.files[form.file_report.name]     # get file
            file_name = f"{data['name'].upper()}-{data['version']}"      # all name loaded file "DRIXDN630YI-3.0_SiC(30kW).csv"
            file_object = _data.stream.read()    # read file

            # parsing file object
            # get only unique components from file_object(readed report_file) [pcb_name, {parameters from file_object}]
            prepared_file_object = pfrd.select_unique_component(file_object, pcb_name=file_name)
            # dict(refdes: category name)
            map_rdcateg = dbt.map_refdes_category()
            # converting a component to write to db
            pcb_components = pfrd.parsing_components(prepared_file_object[1], map_rdcateg)
            # check component on exist in db
            pcb_components_in_db = dbt.exists_components_in_db(pcb_components)  #([exist in db],[not exist in db],): tuple
            # if all components exist in DB
            if not pcb_components_in_db[1]:
                global exists_pcb_comps
                exists_pcb_comps = pcb_components_in_db[0]
            form.name = data['name']
            form.version = data['version']
            form.comment = data["comment"]
            form.count_boards = data["count_boards"]
            print(pcb_components_in_db)
            print(len(pcb_components_in_db[0]), len(pcb_components_in_db[1]))
            return render_template('create/create_pcb.html',
                                   prepared_rep_file=pcb_components_in_db,
                                   title='creation PCBoard',
                                   form=form,
                                   bd=temp_bd)

        elif request.method == "POST" and data['submit_create']:
            new_pcb = PCBoard(name=data['name'],
                              version=data['version'],
                              count_boards=data['count_boards'],
                              comment=data['comment'],)
            print(exists_pcb_comps)    # [{'count': 4, 'id_component'}, {......}, ]
            crud.write_to_table_column(new_pcb)
            print(new_pcb.name, new_pcb.id)

            list_assoc_comp = [AssociatedCompPcb(pcb_id=new_pcb.id,
                                                 comp_id=i['id_component'],
                                                 comp_count=i['count']) for i in exists_pcb_comps]
            crud.write_n_column_to_table(list_assoc_comp)
            # todo if cant create associate table --> delete pcboard and flush err
            flash(f"PCB {data['name']} {data['version']} is created", 'Success')

        return redirect(url_for('create_pcb'))
    temp_bd['quote'] = random_quote()
    return render_template('create/create_pcb.html',
                           title='creation PCBoard',
                           form=form,
                           bd=temp_bd)
