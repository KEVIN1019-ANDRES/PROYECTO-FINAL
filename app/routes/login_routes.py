from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario  # Asegúrate de importar el modelo Usuario
from app import db  # Asegúrate de importar tu objeto db

# Cambiamos el nombre del blueprint a 'auth'
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtiene los datos del formulario
        usuario = request.form.get('nombreU')
        contraseña = request.form.get('contraseña')

        # Busca el usuario en la base de datos por su nombre de usuario
        user = Usuario.query.filter_by(username=usuario).first()

        # Verifica si el usuario existe y si la contraseña es correcta
        if user and user.check_password(contraseña):
            # Inicia la sesión del usuario
            login_user(user)
            
            # Guarda el rol del usuario en la sesión
            session['user_id'] = user.id  # Guarda el id del usuario en la sesión
            session['user_role'] = user.rol  # Guarda el rol del usuario en la sesión

            flash('Inicio de sesión exitoso', 'success')

            # Verifica si el usuario es administrador
            if user.rol == 'admin':
                # Si es administrador, redirige al panel de administración
                return redirect(url_for('admin_index'))  # Ruta del panel de administrador
            else:
                # Si es un cliente regular, redirige a la vista de usuario
                return redirect(url_for('index'))  # Ruta para usuarios regulares
        else:
            # Si las credenciales son incorrectas
            flash('Credenciales inválidas', 'danger')

    return render_template('login/index.html')

@auth_bp.route('/logout')
@login_required
def logout():
    # Elimina las variables de sesión y cierra la sesión del usuario
    session.pop('user_id', None)
    session.pop('user_role', None)
    logout_user()
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('auth.login'))  
# Ruta para el panel de administración (solo accesible por administradores)
@auth_bp.route('/admin')
@login_required
def admin_index():
    # Verifica si el usuario tiene el rol de administrador
    if current_user.rol != 'admin':
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('index'))  # Redirige si no es administrador
    return render_template('producto/index.html')
