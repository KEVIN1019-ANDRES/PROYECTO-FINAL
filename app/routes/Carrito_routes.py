from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_required, current_user
from app.admin.models.producto import Producto
from app.admin.models.vehiculo import Vehiculo
from app.models.Carrito import Carrito
from app import db

bp = Blueprint('carritos', __name__)
carrito_compras = Carrito()
from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('carritos', __name__)

def inicializar_carrito():
    if 'carrito' not in session:
        session['carrito'] = {}

@bp.route('/carrito')
@login_required
def ver_carrito():
    inicializar_carrito()
    items_carrito = []
    total = 0
    for vehiculo_id, cantidad in session['carrito'].items():
        vehiculo = Vehiculo.query.get(vehiculo_id)
        if vehiculo:
            subtotal = vehiculo.precio * cantidad
            items_carrito.append({
                'id': vehiculo.id,
                'nombre': vehiculo.modelo,
                'precio': vehiculo.precio,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
            total += subtotal
    return render_template('carrito/ver_carrito.html', items_carrito=items_carrito, total=total)

@bp.route('/agregar/<int:id>', methods=['POST'])
def agregar_carrito(id):
    cantidad = int(request.form['cantidad'])
    tipo = request.form.get('tipo')
    
    if tipo == 'producto':
        carrito_compras.agregar_producto(producto_id=id, cantidad=cantidad)
    elif tipo == 'vehiculo':
        carrito_compras.agregar_vehiculo(vehiculo_id=id, cantidad=cantidad)
    
    return redirect(url_for('carritos.index'))

@bp.route('/agregar-al-carrito/<int:vehiculo_id>', methods=['POST'])
@login_required
def agregar_al_carrito(vehiculo_id):
    inicializar_carrito()
    cantidad = int(request.form.get('cantidad', 1))
    
    if vehiculo_id in session['carrito']:
        session['carrito'][vehiculo_id] += cantidad
    else:
        session['carrito'][vehiculo_id] = cantidad
    
    session.modified = True
    return jsonify({
        'message': 'Producto agregado al carrito',
        'cantidad_total': sum(session['carrito'].values())
    })

@bp.route('/actualizar-carrito/<int:vehiculo_id>', methods=['POST'])
@login_required
def actualizar_carrito(vehiculo_id):
    inicializar_carrito()
    cantidad = int(request.form.get('cantidad', 0))
    
    if cantidad > 0:
        session['carrito'][str(vehiculo_id)] = cantidad
    else:
        session['carrito'].pop(str(vehiculo_id), None)
    
    session.modified = True
    return redirect(url_for('carritos.ver_carrito'))

@bp.route('/eliminar-del-carrito/<int:vehiculo_id>', methods=['POST'])
@login_required
def eliminar_del_carrito(vehiculo_id):
    inicializar_carrito()
    session['carrito'].pop(str(vehiculo_id), None)
    session.modified = True
    return redirect(url_for('carritos.ver_carrito'))

@bp.route('/cantidad-carrito')
def cantidad_carrito():
    inicializar_carrito()
    cantidad_total = sum(session['carrito'].values())
    return jsonify({'cantidad_total': cantidad_total})

@bp.route('/realizar_compra')
def realizar_compra():
    total = carrito_compras.calcular_total()
    return render_template('realizar_compra.html', total=total)

@bp.route('/generar_factura', methods=['POST'])
def generar_factura():
    total = carrito_compras.calcular_total()
    # Aquí puedes almacenar la información en la base de datos (crear registros en Carrito y Factura)
    # y luego limpiar el carrito de compras
    carrito_compras.carrito = []
    return render_template('factura.html', total=total)

@bp.route('/itemscarrito', methods=['GET', 'POST'])
def tCarrito():
    cantidad_items = carrito_compras.tamañoD()
    print("Cantidad de items en el carrito:", cantidad_items)
    return f"Entra a carrito {cantidad_items} items"