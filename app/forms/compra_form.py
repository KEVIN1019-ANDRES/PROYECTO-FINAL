from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class CompraForm(FlaskForm):
    direccion = StringField('Dirección', validators=[DataRequired(), Length(min=10, max=200)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('Finalizar Compra')
