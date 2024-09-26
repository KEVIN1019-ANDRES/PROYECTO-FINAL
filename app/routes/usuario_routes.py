from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.models.usuario import Usuario  # Asegúrate de importar correctamente el modelo Usuario
from app import db
from werkzeug.security import generate_password_hash
from app.admin.models.vehiculo import Vehiculo

bp = Blueprint('usuarios', __name__)

@bp.route('/admin/dashboard')
def admin_view():
    return render_template('admin/vista_Ad.html')


@bp.route('/cliente/dashboard')
@login_required
def cliente_dashboard():
    return render_template('vista/Vista_Us.html')

@bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    current_app.logger.info("Accediendo al dashboard de administrador")
    try:
        vehiculos = Vehiculo.getItems()
        current_app.logger.info(f"Número de vehículos encontrados: {len(vehiculos)}")
        for v in vehiculos[:5]:  # Muestra los primeros 5 vehículos
            current_app.logger.info(f"Vehículo: {v.marca} {v.modelo}")
        
        return render_template('admin/vista_Ad.html', vehiculos=vehiculos)
    except Exception as e:
        current_app.logger.error(f"Error al obtener vehículos: {str(e)}")
        return render_template('admin/vista_Ad.html', vehiculos=[])

@bp.route('/admin/lista-usuarios')
@login_required
def lista_usuarios():
    if current_user.rol != 'admin':
        flash('No tienes permiso para acceder a esta página', 'danger')
        return redirect(url_for('usuarios.cliente_dashboard'))
    usuarios = Usuario.query.all()
    return render_template('admin/lista_usuarios.html', usuarios=usuarios)

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

@bp.route('/registraru', methods=['GET', 'POST'])
def registraru():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        username = request.form.get('nombreU')
        email = request.form.get('correo')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        contraseña = request.form.get('contraseña')
        confirmar_contraseña = request.form.get('confirmar_contraseña')
        rol = request.form.get('rol')
        
        # Verificar si el usuario o email ya existen
        user_exists = Usuario.query.filter_by(username=username).first()
        email_exists = Usuario.query.filter_by(email=email).first()

        if user_exists:
            flash('El nombre de usuario ya está en uso.', 'danger')
        elif email_exists:
            flash('El correo electrónico ya está registrado.', 'danger')
        elif contraseña != confirmar_contraseña:
            flash('Las contraseñas no coinciden.', 'danger')
        else:
            # Crear nuevo usuario
            new_user = Usuario(
                nombre=nombre,
                username=username,
                email=email,
                telefono=telefono,
                direccion=direccion,
                rol=rol
            )
            new_user.set_password(contraseña)
            db.session.add(new_user)
            db.session.commit()
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login.login'))  # Asegúrate de que 'login.login' es la ruta correcta

    return render_template('login/index.html')  # Asumiendo que tu template de login se llama index.html

# Archivo app/routes/usuario_routes.py
