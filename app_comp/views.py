from app_comp import app
from flask import render_template, redirect, url_for, \
                    flash, request, g, session
from app_comp.models import temp_bd, Category, Pattern, Component, \
                            PCBoard, AssociatedCompPcb
from app_comp.forms import PatternAddForm, ComponentAddForm, \
                            PCBAddForm, CategoryAddForm, SearchForm,\
                            ChangeComponentForm, CollectPCBForm

from app_comp.tools.quotes import random_quote
import app_comp.tools.database_tools as dbt
import app_comp.tools.preparing_filereport_date as pfrd
from decimal import Decimal


crud = dbt.CRUDTable()


@app.before_request
def base():
    g.form_search = SearchForm()
    temp_bd['quote'] = random_quote()
    temp_bd['user'] = 'magos Walentain'
    g.bd = temp_bd


@app.route('/',  methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html", title="Home",)


@app.route('/search', methods=['POST'])
def search_element():
    if g.form_search.validate_on_submit():
        data = g.form_search.data
        text = data['value']
        type_table = data['type_search']
        search_result = dbt.search_text(type_table, text)
        if search_result:
            return render_template('search/search.html',
                                   title='search element',
                                   search_result=search_result,
                                   type_table=type_table,
                                   )
        else:
            flash(f'Value {text} in table {type_table} not exist, try again', 'Warning')
    return render_template('search/search.html',
                           title='search element',
                           search_result=[],
                           type_table='Nothing to look for. Try again.'
                           )


@app.route('/categories/<string:type_category>', methods=['get'])
def categories(type_category='menu'):
    all_cat = crud.read_table_sorted(Category, Category.name)
    category = type_category
    if category != 'menu':
        components_from_category = dbt.get_components_from_category(category, Component)
        if components_from_category:
            return render_template("categories.html",
                                   title='Categories',
                                   all_categories=all_cat,
                                   components_of_category=components_from_category)
        # else:
        #     return redirect(url_for("categories", type_category='menu'))
    #else:
    return render_template("categories.html",
                               title='Categories',
                               all_categories=all_cat)


@app.route('/creation/component', methods=['get', 'post'])
def create_component():
    form = ComponentAddForm()
    form.pattern.choices = [p[0] for p in crud.read_table_all(Pattern.name)]
    form.category.choices = [c[0] for c in crud.read_table_all(Category.name)]
    if form.validate_on_submit():
        all_data = form.data    # get all data from form
        if all_data['unit'] != "None":
            all_data['value'] = f"{all_data['value']}{all_data['unit']}"
        else:
            all_data['value'] = all_data['value'].upper()
        dbt.create_component(all_data)
        flash(f"component {all_data['category']}: {all_data['value']} ({all_data['pattern']}) is created", 'Success')
        return redirect(url_for('create_component'))
    return render_template('create/creation.html',
                           title='Component, Board',
                           form=form)


@app.route("/creation/pattern", methods=['get', 'post'])
def create_pattern():
    form = PatternAddForm()
    if form.validate_on_submit():
        new_pattern = Pattern(name=form.name.data.upper())
        crud.write_to_table_column(new_pattern)
        flash(f'Pattern "{new_pattern}" is created', 'Success')
        return redirect(url_for('create_pattern'))
    return render_template('create/creation.html',
                           title='Pattern',
                           form=form)


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

    return render_template('create/creation.html',
                           title='Category',
                           form=form,)


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
            form.name = data['name'].upper()
            form.version = data['version']
            form.comment = data["comment"]
            form.count_boards = data["count_boards"]
            return render_template('create/create_pcb.html',
                                   prepared_rep_file=pcb_components_in_db,
                                   title='creation PCBoard',
                                   form=form,)

        elif request.method == "POST" and data['submit_create']:
            new_pcb = PCBoard(name=data['name'].upper(),
                              version=data['version'],
                              count_boards=data['count_boards'],
                              comment=data['comment'],)
            # print(exists_pcb_comps)    # [{'count': 4, 'id_component'}, {......}, ]
            crud.write_to_table_column(new_pcb)
            # print(new_pcb.name, new_pcb.id)

            list_assoc_comp = [AssociatedCompPcb(pcb_id=new_pcb.id,
                                                 comp_id=i['id_component'],
                                                 comp_count=i['count']) for i in exists_pcb_comps]
            crud.write_n_column_to_table(list_assoc_comp)
            # todo if cant create associate table --> delete pcboard and flush err
            flash(f"PCB {data['name'].upper()} {data['version']} is created", 'Success')

        return redirect(url_for('create_pcb'))
    return render_template('create/create_pcb.html',
                           title='creation PCBoard',
                           form=form,)


@app.route('/change/<string:id_component>', methods=['get', 'post'])
def change_component(id_component: object):
    compt = crud.read_element_on_id(Component, id_component)
    form_ch = ChangeComponentForm()
    if form_ch.validate_on_submit():
        if request.method == "POST" and form_ch.submit_change.data:
            if form_ch.count.data > 0:
                compt.count = form_ch.count.data
            if form_ch.comment.data:
                compt.comment = form_ch.comment.data
            crud.write_to_table_column(compt)
            flash(f"Component {compt} changed", 'Success')
        elif request.method == "POST" and form_ch.submit_delete.data:
            crud.delete_table_column(compt)
            flash(f"Component {compt} deleted", 'Warning')
            return redirect(url_for('categories', type_category=compt.category_name))
    return render_template("change/component.html",
                           title='change component',
                           component=compt,
                           form=form_ch)


@app.route('/assembly_pcb/<string:pcb_name>/<float:pcb_version>', methods=['get', 'post'])
def list_pcb(pcb_name='pcb', pcb_version=0.0):
    """
    collect of PCB
    """
    all_pcb = crud.read_table_sorted(PCBoard, PCBoard.name)
    if request.method == 'POST':
        data = request.form['rework']
        if data == 'change':
            return redirect(url_for('change_pcb', pcb_name=pcb_name, pcb_version=pcb_version))
        elif data == "collect":
            return redirect(url_for('collect_pcb', pcb_name=pcb_name, pcb_version=pcb_version))
    if pcb_name != 'pcb':
        filter = (PCBoard.name == pcb_name, PCBoard.version == pcb_version)
        pcb = crud.read_table_filter_first(PCBoard, filter)
        components_on_pcb = pcb.get_parameters_as_dict()['components']
        if components_on_pcb:
            return render_template("pcb_view.html",
                                   title='Collect object Printed Circuit Board',
                                   all_pcb=all_pcb,
                                   pcb_obj=pcb,
                                   components_on_pcb=components_on_pcb)
        else:
            return redirect(url_for("list_pcb", pcb_name='pcb', pcb_version=1.0))
    return render_template("pcb_view.html",
                           title="Printed Circuit Board",
                           all_pcb=all_pcb)


@app.route('/assembly_pcb/change/<string:pcb_name>/<float:pcb_version>', methods=['get', 'post'])
def change_pcb(pcb_name, pcb_version):
    filter = (PCBoard.name == pcb_name, PCBoard.version == pcb_version)
    pcb = crud.read_table_filter_first(PCBoard, filter)
    form_pch = ChangeComponentForm()
    if form_pch.validate_on_submit():
        if request.method == "POST" and form_pch.submit_change.data:
            if form_pch.count.data > 0:
                pcb.count_boards = form_pch.count.data
            if form_pch.comment.data:
                pcb.comment = form_pch.comment.data
            crud.write_to_table_column(pcb)
            flash(f"Printed Circuit Board: {pcb} changed", 'Success')
        elif request.method == "POST" and form_pch.submit_delete.data:
            crud.delete_table_column(pcb)
            flash(f"Printed Circuit Board: {pcb} deleted", 'Warning')
            return redirect(url_for('list_pcb', pcb_name='pcb', pcb_version=0))
    return render_template("change/pcb_change.html",
                           title='Change PCB',
                           component=pcb,
                           form=form_pch)


@app.route('/assembly_pcb/collect/<string:pcb_name>/<float:pcb_version>', methods=['get', 'post'])
def collect_pcb(pcb_name, pcb_version):
    _filter = (PCBoard.name == pcb_name, PCBoard.version == pcb_version)
    pcb = crud.read_table_filter_first(PCBoard, _filter)
    parameters_pcb = pcb.get_parameters_as_dict()
    components_filtred = dbt.check_count_component_from_pcb(parameters_pcb['components'], 1)
    form = CollectPCBForm()
    if form.validate_on_submit():
        data = form.data
        print(data)
        n = int(data['count'])
        components_filtred = dbt.check_count_component_from_pcb(parameters_pcb['components'], n)
        if request.method == "POST" and form.submit_check.data:
            print(components_filtred)
            # form.count = form.count.data
            return render_template("pcb_part/pcb_assembly.html",
                                   title='Collect PCB',
                                   f_components_pcb=components_filtred,
                                   parameters_pcb=parameters_pcb,
                                   form=form,
                                   )
        elif request.method == "POST" and form.submit_collect.data:
            print('collect')
            if not components_filtred['component_delta']:
                flash(f"Printed Circuit Board {pcb_name}-v{pcb_version} compiled", 'Warning')
                for i in components_filtred['component_enough']:
                    i[0].count = i[0].count - i[1]
                crud.write_commit()
            return redirect(url_for("list_pcb", pcb_name=pcb_name, pcb_version=pcb_version))
    return render_template("pcb_part/pcb_assembly.html",
                           title='Collect PCB',
                           parameters_pcb=parameters_pcb,
                           f_components_pcb=components_filtred,
                           form=form,
                           )
