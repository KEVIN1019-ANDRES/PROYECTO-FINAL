from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario import Usuario
from app import db
from flask_login import login_user, login_required, logout_user# Asegúrate de importar el modelo Usuario
from werkzeug.security import check_password_hash
from app.forms.login_form import LoginForm

# Cambiamos el nombre del blueprint a 'auth'
bp = Blueprint('login', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Has iniciado sesión correctamente', 'success')
            return redirect(url_for('main.index'))  # o la ruta que uses para tu página principal
        else:
            flash('Email o contraseña incorrectos. Por favor, intenta de nuevo.', 'error')
    return render_template('login/index.html', form=form)


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
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login.login'))

