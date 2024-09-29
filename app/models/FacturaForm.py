from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class FacturaForm(FlaskForm):
    metodo_entrega = SelectField('Método de Entrega', 
        choices=[('domicilio', 'Domicilio'), ('recoger', 'Recoger en tienda')], 
        validators=[DataRequired(message="Por favor, seleccione un método de entrega")])
    
    departamento = StringField('Departamento', 
        validators=[DataRequired(message="El departamento es requerido"), 
                    Length(max=100, message="El departamento no puede exceder los 100 caracteres")])
    
    municipio = StringField('Municipio', 
        validators=[DataRequired(message="El municipio es requerido"), 
                    Length(max=100, message="El municipio no puede exceder los 100 caracteres")])
    
    metodo_pago = SelectField('Método de Pago', 
        choices=[('efectivo', 'Efectivo'), 
                 ('tarjeta', 'Tarjeta de crédito/débito'), 
                 ('transferencia', 'Transferencia bancaria')], 
        validators=[DataRequired(message="Por favor, seleccione un método de pago")])
    
    submit = SubmitField('Procesar Factura')

    def __init__(self, *args, **kwargs):
        super(FacturaForm, self).__init__(*args, **kwargs)
        # Aquí puedes añadir lógica adicional si es necesario
        # Por ejemplo, cargar dinámicamente las opciones de departamentos y municipios
