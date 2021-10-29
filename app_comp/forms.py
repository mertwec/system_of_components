from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired

import app_comp.tools.database_tools as dbt


class ComponentAddForm(FlaskForm):
    value = StringField("Value:", validators=[DataRequired()])
    unit = SelectField('Unit:', choices=dbt.unit_list, default=None)
    tolerance = IntegerField("Tol, %:", default=0)
    voltage = IntegerField("Voltage,V:", default=0)
    power = DecimalField('Power, Wt:', default=0.0)
    count = IntegerField("Count:", validators=[DataRequired()])
    comment = TextAreaField("Comment:")
    pattern = SelectField("Pattern:", choices=dbt.existing_patterns, validators=[DataRequired()])
    category = SelectField("Category:", choices=dbt.existing_categories, validators=[DataRequired()])
    submit = SubmitField('Create component')


class PatternAddForm(FlaskForm):
    name = StringField("Pattern name:", validators=[DataRequired()])
    submit = SubmitField('Create pattern')


class CategoryAddForm(FlaskForm):
    name = StringField("Category:", validators=[DataRequired()])
    submit = SubmitField('Create Category')
