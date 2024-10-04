from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.admin.models.CarruselSlide import CarruselSlide
from app.admin.models.vehiculo import Vehiculo
from app.models.usuario import Usuario
from app.models.factura import Factura
from app.models.FacturaForm import FacturaForm
from flask import session
import secrets
from app import db
from flask_wtf.csrf import generate_csrf

bp = Blueprint('usuarios', __name__)

@bp.route('/cliente/dashboard')
def cliente_dashboard():
    try:
        vehiculos = Vehiculo.query.all()
        current_app.logger.info(f"Número de vehículos encontrados: {len(vehiculos)}")
        imagenes_c = CarruselSlide.query.order_by(CarruselSlide.orden).all()
        print(f"Número de imágenes en el carrusel: {len(imagenes_c)}")
        return render_template('vista/Vista_Us.html', vehiculos=vehiculos, imagenes_c=imagenes_c)
    except Exception as e:
        current_app.logger.error(f"Error al obtener vehículos: {str(e)}")
        return render_template('vista/Vista_Us.html', vehiculos=[], imagenes_c=[])

@bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.rol != 'admin':
        flash('No tienes permiso para acceder a esta página', 'error')
        return redirect(url_for('usuarios.cliente_dashboard'))
    
    try:
        vehiculos = Vehiculo.query.all()
        current_app.logger.info(f"Número de vehículos encontrados: {len(vehiculos)}")
        imagenes_c = CarruselSlide.query.order_by(CarruselSlide.orden).all()
        print(f"Número de imágenes en el carrusel: {len(imagenes_c)}")
        return render_template('admin/vista_Ad.html', vehiculos=vehiculos, imagenes_c=imagenes_c)
    except Exception as e:
        current_app.logger.error(f"Error al obtener vehículos: {str(e)}")
        flash('Hubo un error al cargar los vehículos', 'error')
        return render_template('admin/vista_Ad.html', vehiculos=[])

@bp.route('/admin/lista-usuarios')
@login_required
def lista_usuarios():
    if current_user.rol != 'admin':
        flash('No tienes permiso para acceder a esta página', 'danger')
        return redirect(url_for('usuarios.cliente_dashboard'))
    usuarios = Usuario.query.all()
    csrf_token = secrets.token_hex(16)
    session['csrf_token'] = csrf_token
    return render_template('admin/usuarios/lista_usuarios.html', usuarios=usuarios, csrf_token=csrf_token)

@bp.route('/admin/cambiar-rol/<int:user_id>/<string:new_role>', methods=['POST'])
@login_required
def cambiar_rol(user_id, new_role):
    if current_user.rol != 'admin':
        return jsonify({'success': False, 'message': 'No tienes permiso para realizar esta acción'}), 403
    
    user = Usuario.query.get_or_404(user_id)
    if user == current_user:
        return jsonify({'success': False, 'message': 'No puedes cambiar tu propio rol'}), 400
    
    if new_role not in ['admin', 'cliente']:
        return jsonify({'success': False, 'message': 'Rol no válido'}), 400
    
    user.set_role(new_role)
    return jsonify({'success': True, 'message': f'Rol de {user.username} cambiado a {new_role}'})

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_Us(id):
    if current_user.rol != 'admin':
        flash('No tienes permiso para realizar esta acción', 'error')
        return redirect(url_for('usuarios.cliente_dashboard'))
    
    usuario = Usuario.query.get_or_404(id)
    
    if usuario == current_user:
        flash('No puedes eliminar tu propia cuenta', 'error')
        return redirect(url_for('usuarios.lista_usuarios'))
    
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash(f'Usuario {usuario.username} eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al eliminar usuario: {str(e)}")
        flash('Hubo un error al eliminar el usuario', 'error')
    
    return redirect(url_for('usuarios.lista_usuarios'))

@bp.route('/admin/detalles-usuario/<int:id>', methods=['GET', 'POST'])
@login_required
def detalles_Us(id):
    if current_user.rol != 'admin':
        flash('No tienes permiso para acceder a esta página', 'danger')
        return redirect(url_for('usuarios.cliente_dashboard'))

    usuario = Usuario.query.get_or_404(id)
    
    form = FacturaForm()

    if form.validate_on_submit():
        nueva_factura = Factura(
            usuario_id=usuario.id,
            metodo_entrega=form.metodo_entrega.data,
            departamento=form.departamento.data,
            municipio=form.municipio.data,
            metodo_pago=form.metodo_pago.data,
            total=calcular_total_factura(form)  # Función que debes implementar
        )
        db.session.add(nueva_factura)
        db.session.commit()
        flash('Factura creada correctamente', 'success')
        return redirect(url_for('admin.detalles_Us', id=usuario.id))

    page = request.args.get('page', 1, type=int)
    facturas = usuario.facturas.order_by(Factura.fecha.desc()).paginate(page=page, per_page=10)
    
    return render_template('admin/usuarios/detalles_Us.html', 
                           usuario=usuario, 
                           form=form, 
                           facturas=facturas,
                            csrf_token=generate_csrf())

def calcular_total_factura(form):
    # Implementa la lógica para calcular el total de la factura
    # basándote en los datos del formulario
    return 0  # Placeholder
