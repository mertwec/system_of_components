from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    TextAreaField, SelectField, IntegerField,\
    DecimalField, FileField, FloatField
from wtforms import validators
from wtforms.validators import DataRequired, ValidationError
from app_comp.models import Pattern, Category, Component, PCBoard
import app_comp.tools.database_tools as dbt
from decimal import Decimal


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

    def validate_value(self, value):
        if self.unit.data != "None":
            value = f"{value.data}{self.unit.data}"
        else:
            value = value.data.upper()
        component = Component.query.filter_by(value=value,
                                              pattern_name=self.pattern.data,
                                              tolerance=float(self.tolerance.data)
                                              ).first()
        if component is not None:
            message = f'Component {value} ({self.pattern.data}) {self.tolerance.data}% already exists'
            raise ValidationError(message)

    def validate_unit(self, unit):
        """
        checking if the "unit" parameter matches the "category"
        """
        unit = unit.data
        category = self.category.data
        message = f'unit: {unit} and category:{category.title()} do not correspond!'
        check = {'R': 'resistor',
                 'F': 'capacitor',
                 'z': 'quartz',
                 'H': 'inductance', }
        if unit == "None" and category in check.values():
            raise ValidationError(message)
        elif unit[-1] == 'R' and category != check['R']:
            raise ValidationError(message)
        elif unit[-1] == 'F' and category != check['F']:
            raise ValidationError(message)
        elif unit[-1] == 'H' and category != check['H']:
            raise ValidationError(message)
        elif unit[-1] == 'z' and category != check['z']:
            raise ValidationError(message)
        else:
            print('true', message[:-16])


class PatternAddForm(FlaskForm):
    name = StringField("Pattern name:", validators=[DataRequired()])
    submit = SubmitField('Create pattern')

    def validate_name(self, name):
        pattern = Pattern.query.filter_by(name=name.data.upper()).first()
        if pattern is not None:
            raise ValidationError(f'Pattern {pattern} already exists')


class CategoryAddForm(FlaskForm):
    name = StringField("Category:", validators=[DataRequired()])
    refdes = StringField("RefDes:", validators=[DataRequired()])
    submit = SubmitField('Create Category')

    def validate_name(self, name):
        cat = Category.query.filter_by(name=name.data.lower()).first()
        if cat is not None:
            raise ValidationError(f'Category {cat} already exists')


class PCBAddForm(FlaskForm):
    name = StringField("Name pcb:", validators=[DataRequired()])
    version = FloatField("Version (float):", default=1.0, validators=[DataRequired()])
    count_boards = IntegerField("Count assemble:", default=0)
    comment = TextAreaField("Comment:")
    file_report = FileField("Report file csv:")     #, validators=[Regexp(regex=r'[\S]+\.csv$')])
    submit_create = SubmitField('Create PCB')
    submit = SubmitField('Component check')

    def validate_name(self, name):
        pcb = PCBoard.query.filter_by(name=name.data.upper(), version=float(self.version.data)).first()
        if pcb is not None:
            raise ValidationError(f'PCBoard {pcb} already exists')


class SearchForm(FlaskForm):
    value = StringField("Serach value:", validators=[DataRequired()])
    type_search = SelectField("type", choices=['Component', 'PCBoard', 'Pattern'],
                              validators=[DataRequired()],
                              default='Component')
    search = SubmitField('Search')


class ChangeComponentForm(FlaskForm):
    count = IntegerField("New Count:", default=-1)
    comment = TextAreaField("New Commentary:", default=None)
    submit_change = SubmitField('Change')
    submit_delete = SubmitField('Delete')


class CollectPCBForm(FlaskForm):
    count = IntegerField("Count collected board:", default=1)
    submit_check = SubmitField('Check components')
    submit_collect = SubmitField('Collect board')
    # submit_change = SubmitField('Change Commentary')
