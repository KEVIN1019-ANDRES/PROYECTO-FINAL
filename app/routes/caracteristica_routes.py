import re
from flask import Blueprint, render_template, abort
from app.admin.models.vehiculo import Vehiculo

bp = Blueprint('caracteristicas', __name__)

@bp.route('/caracteristicas/vehiculo/<int:id>', methods=['GET'])
def index(id):
    vehiculo = Vehiculo.query.filter_by(id=id).first_or_404()
    return render_template('caracteristicas/index.html', vehiculo=vehiculo)
