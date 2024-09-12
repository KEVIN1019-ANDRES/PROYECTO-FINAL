from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.usuario import Usuario  # Asegúrate de importar correctamente el modelo Usuario
from app import db

usuario_routes = Blueprint('usuario_routes', __name__)

@usuario_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono') 
        nombreu = request.form.get('nombreU')
        contraseña = request.form.get('contraseña')
        direccion = request.form.get('direccion')  # Añade dirección si es parte del formulario
        
        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(email=correo).first():
            flash('El correo ya está registrado.')
            return redirect(url_for('usuario_routes.register'))
        
        new_user = Usuario(
            username=nombreu,
            email=correo,
            telefono=telefono,
            direccion=direccion if direccion else '',  # Asignar dirección solo si está presente
            rol='cliente'  # Cliente por defecto, puedes cambiar a admin manualmente si lo deseas
        )
        new_user.set_password(contraseña)  # Encriptar la contraseña
        db.session.add(new_user)
        db.session.commit()
        flash('Registro exitoso')
        return redirect(url_for('usuario_routes.login'))  # Redirigir al login después de registro
    
    return render_template('register.html')

@usuario_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        
        user = Usuario.query.filter_by(email=email).first()
        if user and user.check_password(contraseña):
            # Autenticación exitosa, redirige al usuario
            flash('Inicio de sesión exitoso')
            return redirect(url_for('home'))  # Redirige a una página protegida o a la página principal
        else:
            flash('Credenciales inválidas')
    
    return render_template('login.html')  # Debes tener una plantilla login.html para el inicio de sesión
 