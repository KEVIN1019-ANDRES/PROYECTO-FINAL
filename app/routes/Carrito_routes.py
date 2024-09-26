from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.admin.models.producto import Producto
from app.admin.models.vehiculo import Vehiculo
from app.models.Carrito import Carrito

bp = Blueprint('carritos', __name__)
carrito_compras = Carrito()


@bp.route('/ListarProductos')
def index():
    productos = carrito_compras.getItems()
    data = Vehiculo.getItems()
    return render_template('producto/list.html', data=data, productos=productos)


@bp.route('/ListarCarrito')
def listar():
    items = carrito_compras.getItems()  
    return render_template('productos/List.html', items=items)


@bp.route('/agregar/<int:id>', methods=['POST'])
def agregar_al_carrito(id):
    cantidad = int(request.form['cantidad'])
    tipo = request.form.get('tipo')
    
    if tipo == 'producto':
        carrito_compras.agregar_producto(producto_id=id, cantidad=cantidad)
    elif tipo == 'vehiculo':
        carrito_compras.agregar_vehiculo(vehiculo_id=id, cantidad=cantidad)
    
    return redirect(url_for('carritos.index'))


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