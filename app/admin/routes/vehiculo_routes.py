import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from werkzeug.utils import secure_filename
from flask import current_app, flash, redirect, url_for
from flask import current_app as app
from app.admin.models.vehiculo import Vehiculo
from app import db

bp = Blueprint('vehiculo', __name__)


def is_valid_filename(filename):
    """Validar el nombre del archivo para evitar caracteres peligrosos."""
    return re.match(r'^[\w\-\.]+$', filename) is not None

def is_valid_file(filename):
    """Verificar si el archivo tiene una extensión permitida."""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@bp.route('/vehiculo/index')
def index():
    data = Vehiculo.query.all()
    return render_template('admin/vista_Ad.html', data=data)

@bp.route('/vehiculo/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        año = request.form.get('año')
        descripcion = request.form.get('descripcion')
        color = request.form.get('color')
        precio = request.form.get('precio')
        precio_anterior = request.form.get('precio_anterior')
        cilindraje = request.form.get('cilindraje')
        imagen = request.files.get('imagen')

        # Validación de campos
        if not (marca and modelo and descripcion and color and año and precio and cilindraje):
            return "Todos los campos son requeridos", 400

        if not imagen or not is_valid_file(imagen.filename):
            return "La imagen es requerida y debe ser de un tipo permitido", 400

        # Crear una carpeta para la marca si no existe
        img_folder = os.path.join(app.root_path, 'static', 'img/vehiculos', marca)
        os.makedirs(img_folder, exist_ok=True)

        # Guardar la imagen en el directorio correspondiente
        imagen_filename = secure_filename(imagen.filename)
        imagen_path = os.path.join(img_folder, imagen_filename)
        imagen.save(imagen_path)

        # Crear un nuevo vehículo y guardarlo en la base de datos
        new_vehiculo = Vehiculo(
            marca=marca,
            modelo=modelo,
            descripcion=descripcion,
            color=color,
            año=año,
            precio=precio,
            precio_anterior=precio_anterior,
            cilindraje=cilindraje,
            imagen=imagen_filename
        )
        db.session.add(new_vehiculo)
        db.session.commit()

        return redirect(url_for('admin.vista_Ad'))

    return render_template('admin/add.html')


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    vehiculo = Vehiculo.query.get_or_404(id)

    if request.method == 'POST':
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        año = request.form.get('año')
        descripcion = request.form.get('descripcion')
        color = request.form.get('color')
        precio = request.form.get('precio')
        precio_anterior = request.form.get('precio_anterior')
        cilindraje = request.form.get('cilindraje')
        imagen = request.files.get('imagen')

        # Validación de campos
        if not (marca and modelo and descripcion and color and año and precio and cilindraje):
            return "Todos los campos son requeridos", 400

        # Actualizar los atributos del vehículo
        vehiculo.marca = marca
        vehiculo.modelo = modelo
        vehiculo.año = año
        vehiculo.descripcion = descripcion
        vehiculo.color = color
        vehiculo.precio = precio
        vehiculo.precio_anterior = precio_anterior
        vehiculo.cilindraje = cilindraje

        if imagen and is_valid_file(imagen.filename):
            # Crear una carpeta para la marca si no existe
            img_folder = os.path.join(app.root_path, 'static', 'img/vehiculos', marca)
            os.makedirs(img_folder, exist_ok=True)

            # Guardar la nueva imagen
            imagen_filename = secure_filename(imagen.filename)
            imagen_path = os.path.join(img_folder, imagen_filename)
            imagen.save(imagen_path)
            vehiculo.imagen = imagen_filename
        elif imagen:
            abort(400, description="Tipo de archivo no permitido")

        db.session.commit()
        return redirect(url_for('admin.vista_Ad'))

    # Construir la URL de la i
    return render_template('admin/edit.html', vehiculo=vehiculo)


@bp.route('/delete/<int:id>')
def delete(id):
    print(f"Intentando eliminar vehículo con ID: {id}")  # Log para depuración
    vehiculo = Vehiculo.query.get_or_404(id)

    # Obtener el nombre del archivo de la imagen
    imagen_filename = vehiculo.imagen
    
    # Eliminar el registro de la base de datos
    db.session.delete(vehiculo)
    db.session.commit()
    
    # Eliminar el archivo de imagen del sistema de archivos si existe
    if imagen_filename:
        # Asume que la imagen está en la carpeta 'static/img'
        img_folder = os.path.join(app.root_path, 'static', 'img/vehiculos', vehiculo.marca)
        imagen_path = os.path.join(img_folder, imagen_filename)
        
        if os.path.isfile(imagen_path):
            os.remove(imagen_path)
    
    return redirect(url_for('admin.vista_Ad'))


@bp.route('/<int:id>')
def detail(id):
    """Mostrar los detalles de un vehículo."""
    vehiculo = Vehiculo.query.get_or_404(id)
    return render_template('detail.html', vehiculo=vehiculo)
