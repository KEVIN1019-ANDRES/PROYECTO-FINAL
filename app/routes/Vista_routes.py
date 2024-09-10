from flask import Blueprint, render_template
from app.admin.models.vehiculo import Vehiculo
from flask import Blueprint, render_template, request, redirect, url_for, jsonify


bp = Blueprint('moto_details', __name__)

@bp.route('/')
def index():
    data = Vehiculo.query.all()
    return render_template('vista/index.html', data=data)
