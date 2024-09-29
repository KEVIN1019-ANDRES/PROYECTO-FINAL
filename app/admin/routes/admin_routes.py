from flask import Blueprint, render_template
from app.admin.models.vehiculo import Vehiculo

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/vista_Ad')
def vista_Ad():
    vehiculos = Vehiculo.query.all()
    return render_template('admin/vista_Ad.html', vehiculos=vehiculos)