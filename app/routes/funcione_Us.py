from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

bp = Blueprint('funciones_Us', __name__)

@bp.route('/perfil')
@login_required
def perfil():
    return render_template('usuarios/perfil.html')

@bp.route('/direcciones')
@login_required
def direcciones():
    return render_template('usuarios/direcciones.html')

@bp.route('/pedidos')
@login_required
def pedidos():
    return render_template('usuarios/pedidos.html')

@bp.route('/favoritos')
@login_required
def favoritos():
    return render_template('usuarios/favoritos.html')