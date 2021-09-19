from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, TextAreaField
from wtforms.validators import DataRequired


class ComponentAddForm(FlaskForm):
    value = StringField("Value:", validators=[DataRequired()])
    unit = StringField("Unit:")
    tolerance = DecimalField("Tol:")
    count = DecimalField("Count:", default=0, validators=[DataRequired()])
    pattern = StringField('Pattern:', validators=[DataRequired()])
    category = StringField("Category:", validators=[DataRequired()])
    comment = TextAreaField("Comment:")

    submit = SubmitField('Create component')


class PatternAddForm(FlaskForm):
    name = StringField("Pattern name:", validators=[DataRequired()])
    submit = SubmitField('Create pattern')
