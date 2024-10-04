import re
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app.admin.models.vehiculo import Vehiculo
from werkzeug.utils import secure_filename
from flask import current_app as app
from app.admin.models.CarruselSlide import CarruselSlide
import os
from app import db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/vista_Ad')
def vista_Ad():
    vehiculos = Vehiculo.query.all()
    imagenes_c = CarruselSlide.query.order_by(CarruselSlide.orden).all()
    print(f"Número de imágenes en el carrusel: {len(imagenes_c)}")
    for imagen in imagenes_c:
        print(f"Imagen: {imagen.imagen_nombre}")
    return render_template('admin/vista_Ad.html', vehiculos=vehiculos, imagenes_c=imagenes_c)


def is_valid_filename(filename):
    """Validar el nombre del archivo para evitar caracteres peligrosos."""
    return re.match(r'^[\w\-\.]+$', filename) is not None

def is_valid_file(filename):
    """Verificar si el archivo tiene una extensión permitida."""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@bp.route('/agregar_carrusel', methods=['GET', 'POST'])
def agregar_carrusel():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        ruta = request.form.get('ruta')
        orden = request.form.get('orden')
        imagen = request.files.get('imagen_N')
        
        print(f"Titulo: {titulo}")
        print(f"Descripción: {descripcion}")
        print(f"Ruta: {ruta}")
        print(f"Orden: {orden}")
        print(f"Imagen: {imagen}")
        
        if not (titulo and descripcion and orden and imagen):
            flash('Todos los campos son requeridos', 'error')
            return redirect(url_for('admin.agregar_carrusel'))
        
        if not is_valid_file(imagen.filename):
            flash('El archivo de imagen no es válido', 'error')
            return redirect(url_for('admin.agregar_carrusel'))
        
        filename = secure_filename(imagen.filename)
        imagen_path = os.path.join(current_app.root_path, 'static', 'img', 'carrusel', filename)
        
        # Asegúrate de que el directorio existe
        os.makedirs(os.path.dirname(imagen_path), exist_ok=True)
        
        imagen.save(imagen_path)
        
        print(f"Imagen guardada en: {imagen_path}")  # Añade este log
        
        nueva_imagen = CarruselSlide(
            titulo=titulo,
            descripcion=descripcion,
            ruta=ruta,
            orden=int(orden),
            imagen_nombre=filename
        )
        
        db.session.add(nueva_imagen)
        db.session.commit()
        
        flash('Diapositiva agregada exitosamente', 'success')
        return redirect(url_for('admin.vista_Ad'))
    
    return render_template('admin/carrucel/agregarc.html')