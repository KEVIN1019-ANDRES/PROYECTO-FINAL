from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario import Usuario
from app import db
from flask_login import login_user, login_required, logout_user, current_user# Asegúrate de importar el modelo Usuario
from werkzeug.security import check_password_hash



# Cambiamos el nombre del blueprint a 'auth'
bp = Blueprint('login', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login.login'))

    if request.method == 'POST':
        username = request.form.get('nombreU')
        password = request.form.get('contraseña')
        
        user = Usuario.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Has iniciado sesión correctamente', 'success')
            
            # Redirige basado en el rol del usuario
            if user.rol == 'admin':
                return redirect(url_for('usuarios.admin_dashboard'))
            else:
                return redirect(url_for('usuarios.cliente_dashboard'))
        else:
            flash('Usuario o contraseña incorrectos. Por favor, intenta de nuevo.', 'error')
    
    return render_template('login/index.html')


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
            return redirect(url_for('usuarios.registraru'))
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
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))

