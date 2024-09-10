import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from werkzeug.utils import secure_filename
from flask import current_app as app
from app.admin.models.producto import Producto
from app import db

bp = Blueprint('producto', __name__)    

def is_valid_filename(filename):
    # Validar el nombre del archivo para evitar caracteres peligrosos
    return re.match(r'^[\w\-\.]+$', filename) is not None

def is_valid_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@bp.route('/productos/index')
def index():
    data = Producto.query.all()
    return render_template('producto/index.html', data=data)

@bp.route('/producto/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('Precio')  # Asegúrate de que este nombre coincida con el nombre del campo en el formulario HTML
        producto = request.form.get('tipo_producto')  # Cambiado de `producto` a `tipo_producto`
        stock = request.form.get('stokcproducto')  # Asegúrate de que este nombre coincida con el nombre del campo en el formulario HTML
        descripcion = request.form.get('descripcion')
        producto_imagen = request.files.get('producto_imagen')  # Actualizado para que coincida con el nombre del campo en el formulario HTML

        # Validación de campos
        if not producto_imagen or not is_valid_file(producto_imagen.filename):
            return "La imagen es requerida y debe ser de un tipo permitido", 400

        # Crear una carpeta para la marca si no existe
        img_folder = os.path.join(app.root_path, 'static', 'img/productos', producto)
        os.makedirs(img_folder, exist_ok=True)

        # Guardar la imagen en el directorio correspondiente
        imagen_filename = secure_filename(producto_imagen.filename)
        imagen_path = os.path.join(img_folder, imagen_filename)
        producto_imagen.save(imagen_path)

        # Crear un nuevo producto y guardarlo en la base de datos
        new_producto = Producto(nombre=nombre, precio=precio, producto=producto, descripcion=descripcion, stock=stock, producto_imagen=producto_imagen)
        db.session.add(new_producto)
        db.session.commit()

        return redirect(url_for('producto.index'))

    return render_template('producto/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    producto = Producto.query.get_or_404(id)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        producto_nombre = request.form.get('producto')
        stock = request.form.get('stock')
        descripcion = request.form.get('descripcion')
        imagen = request.files.get('imagen')

        # Validación de campos
        if not (nombre and precio and producto_nombre and descripcion and stock):
            return "Todos los campos son requeridos", 400
        
        # Actualizar los atributos del producto
        producto.nombre = nombre
        producto.precio = precio
        producto.producto = producto_nombre
        producto.descripcion = descripcion
        producto.stock = stock

        if imagen and is_valid_file(imagen.filename):
            # Crear una carpeta para la marca si no existe
            img_folder = os.path.join(app.root_path, 'static', 'img/productos', producto_nombre)
            os.makedirs(img_folder, exist_ok=True)
            
            # Guardar la nueva imagen
            imagen_filename = secure_filename(imagen.filename)
            imagen_path = os.path.join(img_folder, imagen_filename)
            imagen.save(imagen_path)
            producto.imagen = imagen_filename
        elif imagen:
            abort(400, description="Tipo de archivo no permitido")

        db.session.commit()
        return redirect(url_for('producto.index'))
    
    return render_template('producto/edit.html', producto=producto)

@bp.route('/delete/<int:id>')
def delete(id):
    producto = Producto.query.get_or_404(id)

    # Obtener el nombre del archivo de la imagen
    imagen_filename = producto.imagen
    
    # Eliminar el registro de la base de datos
    db.session.delete(producto)
    db.session.commit()
    
    # Eliminar el archivo de imagen del sistema de archivos si existe
    if imagen_filename:
        img_folder = os.path.join(app.root_path, 'static', 'img', producto.producto)
        imagen_path = os.path.join(img_folder, imagen_filename)
        
        if os.path.isfile(imagen_path):
            os.remove(imagen_path)
    
    return redirect(url_for('producto.index'))
