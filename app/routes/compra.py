from flask import Blueprint, render_template, redirect, url_for, session
from app import db
from app.forms.compra_form import CompraForm
from app.models.usuario import Usuario

# Definir el blueprint
compra_bp = Blueprint('compra', __name__)

@compra_bp.route('/iniciar_compra')
def iniciar_compra():
    usuario = Usuario.query.get(session.get('user_id'))

    if not usuario.direccion:
        return redirect(url_for('compra.compra'))
    
    # Continuar con la compra si ya tiene una dirección
    return redirect(url_for('compra.procesar_compra'))

@compra_bp.route('/compra', methods=['GET', 'POST'])
def compra():
    form = CompraForm()
    usuario = Usuario.query.get(session.get('user_id'))

    if form.validate_on_submit():
        usuario.direccion = form.direccion.data
        usuario.telefono = form.telefono.data
        db.session.commit()
        # Procesar la compra aquí
        return redirect(url_for('compra.compra_exitosa'))

    return render_template('compra/compra.html', form=form)

# Si tienes más rutas relacionadas con la compra, agrégalas aquí
