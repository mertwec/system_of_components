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
    tolerance = IntegerField("Tol, %:", default=0)
    voltage = IntegerField("Voltage,V:", default=0)
    power = DecimalField('Power, Wt:', default=0.0)
    count = IntegerField("Count:", default=0)
    comment = TextAreaField("Comment:")
    pattern = SelectField("Pattern:", choices=dbt.existing_patterns, validators=[DataRequired()])
    category = SelectField("Category:", choices=dbt.existing_categories, validators=[DataRequired()])
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
    version = DecimalField("Version (float):", default=1.0, validators=[DataRequired()])
    count_boards = IntegerField("Count:", default=0)
    comment = TextAreaField("Comment:")
    file_report = FileField("Report file csv:")     #, validators=[Regexp(regex=r'[\S]+\.csv$')])
    submit = SubmitField('Create printed circuit board')
