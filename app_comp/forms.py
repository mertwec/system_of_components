from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    TextAreaField, SelectField, IntegerField,\
    DecimalField, FileField, FloatField
from wtforms import validators
from wtforms.validators import DataRequired, Regexp

import app_comp.tools.database_tools as dbt


class ComponentAddForm(FlaskForm):
    value = StringField("Value:", validators=[DataRequired()])
    unit = SelectField('Unit:', choices=dbt.unit_list, default=None)
    tolerance = DecimalField("Tol, %:", default=0.0)
    voltage = IntegerField("Voltage,V:", default=0)
    power = DecimalField('Power, Wt:', default=0.0)
    count = IntegerField("Count:", default=0)
    comment = TextAreaField("Comment:")
    pattern = SelectField("Pattern:", choices=[], validators=[DataRequired()])
    category = SelectField("Category:", choices=[], validators=[DataRequired()])
    submit = SubmitField('Create component')


class PatternAddForm(FlaskForm):
    name = StringField("Pattern name:", validators=[DataRequired()])
    submit = SubmitField('Create pattern')


class CategoryAddForm(FlaskForm):
    name = StringField("Category:", validators=[DataRequired()])
    refdes = StringField("RefDes:", validators=[DataRequired()])
    submit = SubmitField('Create Category')


class PCBAddForm(FlaskForm):
    name = StringField("Name pcb:", validators=[DataRequired()])
    version = FloatField("Version (float):", default=1.0, validators=[DataRequired()])
    count_boards = IntegerField("Count of board:", default=0)
    comment = TextAreaField("Comment:")
    file_report = FileField("Report file csv:")     #, validators=[Regexp(regex=r'[\S]+\.csv$')])
    submit_create = SubmitField('Create PCB')
    submit = SubmitField('Component check')

#
# class SearchComponent(FlaskForm):
#     value = StringField('Value:', validators=[DataRequired()])
#     category = SelectField("Category:", choices=[], default=None)
#     search = SubmitField('Search component')
#     change_comp = SubmitField('Change component')
#
#
# class SearchPCB(FlaskForm):
#     value = StringField('Value:', validators=[DataRequired()])
#     version = StringField('version', default=None)
#     search = SubmitField('Search PCB')


class Search(FlaskForm):
    value = StringField("Value:", validators=[DataRequired()])
    search = SubmitField('Search')
