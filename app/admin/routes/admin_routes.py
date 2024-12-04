import re
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app.admin.models.vehiculo import Vehiculo
from app.admin.models.producto import Producto
from werkzeug.utils import secure_filename
from flask import current_app as app
from flask_login import login_user, login_required, logout_user, current_user# Asegúrate de importar el modelo Usuario
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

@bp.route('/admin/accesorios',  methods=['GET'])
@login_required
def Accesorios_Ad():
    productos = Producto.query.all()
    imagenes_c = CarruselSlide.query.order_by(CarruselSlide.orden).all()
    print(f"Número de imágenes en el carrusel: {len(imagenes_c)}")
    for imagen in imagenes_c:
        imagen_path = os.path.join(current_app.root_path, 'static', 'img', 'carrusel', 'productos', imagen.imagen_nombre)
        print(f"Ruta completa de la imagen: {imagen_path}")
        print(f"Imagen: {imagen.imagen_nombre}, Título: {imagen.titulo}, Ruta: {imagen.ruta}")
        if os.path.exists(imagen_path):
            print(f"Imagen encontrada: {imagen_path}")
        else:
            print(f"Imagen no encontrada: {imagen_path}")
    return render_template('admin/Accesorios_Ad.html', productos=productos , imagenes_c=imagenes_c)


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
        categoria = request.form.get('categoria')  # Nuevo campo para la categoría
        
        # Validaciones
        if not (titulo and descripcion and orden and imagen and categoria):
            flash('Todos los campos son requeridos', 'error')
            return redirect(url_for('admin.agregar_carrusel'))
        
        if not is_valid_file(imagen.filename):
            flash('El archivo de imagen no es válido', 'error')
            return redirect(url_for('admin.agregar_carrusel'))
        
        filename = secure_filename(imagen.filename)
        
        # Determinar la ruta de la imagen según la categoría
        if categoria == 'vehiculos':
            imagen_path = os.path.join(current_app.root_path, 'static', 'img', 'carrucel', 'vehiculos', filename)
        elif categoria == 'productos':
            imagen_path = os.path.join(current_app.root_path, 'static', 'img', 'carrucel', 'productos', filename)
        else:
            flash('Categoría no válida', 'error')
            return redirect(url_for('admin.agregar_carrusel'))
        
        # Asegúrate de que el directorio existe
        os.makedirs(os.path.dirname(imagen_path), exist_ok=True)
        
        imagen.save(imagen_path)
        
        nueva_imagen = CarruselSlide(
            titulo=titulo,
            descripcion=descripcion,
            ruta=ruta,
            orden=int(orden),
            imagen_nombre=filename,
            categoria=categoria
        )
        
        db.session.add(nueva_imagen)
        db.session.commit()
        
        flash('Diapositiva agregada exitosamente', 'success')
        return redirect(url_for('admin.vista_Ad'))
    
    return render_template('admin/carrucel/agregarc.html')


