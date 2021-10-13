from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, TextAreaField, SelectField
from wtforms.validators import DataRequired


existing_patterns = []
existing_categories = []


class ComponentAddForm(FlaskForm):
    value = StringField("Value:", validators=[DataRequired()])
    count = DecimalField("Count:", default=0, validators=[DataRequired()])
    unit = StringField("Unit:")
    tolerance = DecimalField("Tol:")
    pattern = SelectField("Pattern:", choices=existing_patterns, validators=[DataRequired()])
    category = SelectField("Category:", choices=existing_categories, validators=[DataRequired()])
    comment = TextAreaField("Comment:")
    submit = SubmitField('Create component')


class PatternAddForm(FlaskForm):
    name = StringField("Pattern name:", validators=[DataRequired()])
    submit = SubmitField('Create pattern')


class CategoryAddForm(FlaskForm):
    name = StringField("Category:", validators=[DataRequired()])
    submit = SubmitField('Create Category')
