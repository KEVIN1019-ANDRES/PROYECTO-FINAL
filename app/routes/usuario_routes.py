from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.usuario import Usuario  
from app import db

bp = Blueprint('usuarios', __name__)

@bp.route('/cliente/dashboard')
def cliente_dashboard():
    return render_template('cliente/vista.html')

@bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')


@bp.route('/registraru', methods=['GET', 'POST'])
def register():
    print("entra a register")
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        nombreu = request.form.get('nombreU')
        contraseña = request.form.get('contraseña')
        
        # Verificar si el correo ya está registrado
        if Usuario.query.filter_by(email=correo).first():
            flash('El correo ya está registrado.')
            return redirect(url_for('login.login'))
        
        # Crear un nuevo usuario
        new_user = Usuario(
            username=nombreu,
            email=correo,
            telefono=telefono,
            direccion='',  # Puedes agregar un campo para la dirección en el formulario si lo deseas
            rol='cliente'  # Por defecto asignamos el rol 'cliente'
        )
        new_user.set_password(contraseña)  # Encriptar la contraseña
        db.session.add(new_user)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('login.login'))  # Redirigir a la página de login
    
    return render_template('login/index.html')  # Asegúrate de tener la plantilla register.html




@bp.route('/recuperar_contraseña', methods=['GET', 'POST'])
def recuperar_contraseña():
    if request.method == 'POST':
        correo = request.form.get('correo')
        
        # Verificar si el correo está registrado
        usuario = Usuario.query.filter_by(email=correo).first()
        if not usuario:
            flash('El correo no está registrado.')
            return redirect(url_for('usuarios.recuperar_contraseña'))
        
        # Generar un token para restablecer la contraseña
        token = usuario.get_reset_password_token()
        
        # Enviar un correo electrónico con el token de restablecimiento de contraseña}
        send_email('Recuperar Contraseña',
                sender='noreply@demo.com',
                recipients=[usuario.email],
                text_body=render_template('email/reset_password.txt', usuario=usuario, token=token),
                  
        
        flash('Se ha enviado un correo con las instrucciones para recuperar la contraseña.')
        return redirect(url_for('usuarios.login'))
    
    return render_template('login/contra.html')
