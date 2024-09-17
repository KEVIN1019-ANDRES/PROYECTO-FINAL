from flask import Blueprint, render_template, request
from app.admin.models.vehiculo import Vehiculo

bp = Blueprint('moto_details', __name__)

@bp.route('/')
def index():
    # Obtener el número de página, por defecto será la primera
    page = request.args.get('page', 1, type=int)

    # Obtener el término de búsqueda del usuario, si existe
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1,  type=int)

    # Filtrar vehículos basados en la consulta de búsqueda
    print(f"Entra el index -----------{search_query}----   ---------------serach queresafadf")
    if search_query:
        vehiculos = Vehiculo.query.filter(
            Vehiculo.marca.ilike(f'%{search_query}%') |
            Vehiculo.modelo.ilike(f'%{search_query}%') |
            Vehiculo.color.ilike(f'%{search_query}%')
        ).paginate(page=page, per_page=10)
    else:
        vehiculos = Vehiculo.query.paginate(page=page, per_page=10)


    # Renderizar la vista principal con los resultados paginados
    return render_template('vista/index.html', vehiculos=vehiculos)
