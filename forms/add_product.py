from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddProduct(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = StringField('Свойства', validators=[DataRequired()])
    count = StringField('Количество', validators=[DataRequired()])
    submit = SubmitField('Войти')