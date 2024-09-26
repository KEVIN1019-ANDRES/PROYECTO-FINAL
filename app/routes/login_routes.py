from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario import Usuario
from app import db
from flask_login import login_user, login_required, logout_user# Asegúrate de importar el modelo Usuario

# Cambiamos el nombre del blueprint a 'auth'
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtiene los datos del formulario
        usuario = request.form.get('nombreU')
        contraseña = request.form.get('contraseña')
        
        user = Usuario.query.filter_by(username=usuario).first()
        
        if user and user.check_password(contraseña):
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            
            if user.rol == 'admin':
                return redirect(url_for('usuarios.admin_dashboard'))
            else:
                return redirect(url_for('usuarios.cliente_dashboard'))
        else:
            # Si las credenciales son incorrectas
            flash('Credenciales inválidas', 'danger')
    
    return render_template('login/index.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login.login'))

