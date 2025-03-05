from flask import Blueprint, render_template, current_app, redirect, url_for
from app.admin.models.vehiculo import Vehiculo
from flask_login import login_required, current_user
from app.admin.models.producto import Producto
from app.admin.models.CarruselSlide import CarruselSlide
import os

bp = Blueprint('vista', __name__)

@bp.route('/')
def vista():
    # Verificar si el usuario está autenticado
    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))  # Redirigir a la página de inicio de sesión

    vehiculos = Vehiculo.query.all()
    imagenes_c = CarruselSlide.query.filter_by(categoria='vehiculos').order_by(CarruselSlide.orden).all()
    print(f"Número de imágenes en el carrusel: {len(imagenes_c)}")
    for imagen in imagenes_c:
        imagen_path = os.path.join(current_app.root_path, 'static', 'img', 'carrucel', 'vehiculos', imagen.imagen_nombre)
        print(f"Ruta completa de la imagen: {imagen_path}")
        print(f"Imagen: {imagen.imagen_nombre}, Título: {imagen.titulo}, Ruta: {imagen.ruta}")
        if os.path.exists(imagen_path):
            print(f"Imagen encontrada: {imagen_path}")
        else:
            print(f"Imagen no encontrada: {imagen_path}")
    return render_template('vista/vista_Us.html', vehiculos=vehiculos, imagenes_c=imagenes_c, usuario=current_user)

@bp.route('/accesorios', methods=['GET'])
@login_required
def Accesorios():
    productos = Producto.query.all()
    imagenes_c = CarruselSlide.query.filter_by(categoria='productos').order_by(CarruselSlide.orden).all()
    print(f"Número de imágenes en el carrusel: {len(imagenes_c)}")
    for imagen in imagenes_c:
        imagen_path = os.path.join(current_app.root_path, 'static', 'img', 'carrucel', 'productos', imagen.imagen_nombre)
        print(f"Ruta completa de la imagen: {imagen_path}")
        print(f"Imagen: {imagen.imagen_nombre}, Título: {imagen.titulo}, Ruta: {imagen.ruta}")
        if os.path.exists(imagen_path):
            print(f"Imagen encontrada: {imagen_path}")
        else:
            print(f"Imagen no encontrada: {imagen_path}")
    return render_template('vista/Accesorios_Us.html', productos=productos, imagenes_c=imagenes_c)

