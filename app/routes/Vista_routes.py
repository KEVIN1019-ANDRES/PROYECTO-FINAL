from flask import Blueprint, render_template, current_app
from app.admin.models.vehiculo import Vehiculo
from app.admin.models.CarruselSlide import CarruselSlide
import os

bp = Blueprint('vista', __name__)

@bp.route('/')
def vista():
    vehiculos = Vehiculo.query.all()
    imagenes_c = CarruselSlide.query.order_by(CarruselSlide.orden).all()
    print(f"Número de imágenes en el carrusel: {len(imagenes_c)}")
    for imagen in imagenes_c:
        imagen_path = os.path.join(current_app.root_path, 'static', 'img', 'carrusel', imagen.imagen_nombre)
        print(f"Ruta completa de la imagen: {imagen_path}")
        print(f"Imagen: {imagen.imagen_nombre}, Título: {imagen.titulo}, Ruta: {imagen.ruta}")
        if os.path.exists(imagen_path):
            print(f"Imagen encontrada: {imagen_path}")
        else:
            print(f"Imagen no encontrada: {imagen_path}")
    return render_template('vista/vista_Us.html', vehiculos=vehiculos, imagenes_c=imagenes_c)