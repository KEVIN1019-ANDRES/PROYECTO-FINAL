from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.usuario import Usuario  
from flask_mail import Message, Mail
from app import mail
from app import db

bp = Blueprint('usuarios', __name__)

@bp.route('/cliente/dashboard')
def cliente_dashboard():
    return render_template('cliente/vista.html')

@bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')


@bp.route('/registrar', methods=['GET', 'POST'])
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
            nombre =nombre,
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


@bp.route('/restablecer_contraseña', methods=['GET', 'POST'])
def restablecer_contraseña():
    if request.method == 'POST':
        correo = request.form.get('correo')
        
        # Verificar si el correo está registrado
        usuario = Usuario.query.filter_by(email=correo).first()
        if not usuario:
            flash('El correo no está registrado.')
            return redirect(url_for('usuarios.restablecer_contraseña'))
        
        # Generar un token de restablecimiento de contraseña
        token = usuario.get_reset_password_token()
        
        # Enviar el correo electrónico con el enlace de restablecimiento de contraseña
        send_reset_email(usuario, token)
        flash('Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña.')
        return redirect(url_for('login.login'))
    
    return render_template('auth/restablecer_contraseña.html')

def send_reset_email(usuario, token):
    
    
    msg = Message('Restablecer Contraseña',
                  sender='noreply@demo.com',
                  recipients=[usuario.email])
    msg.body = f'''Para restablecer tu contraseña, visita el siguiente enlace:
{url_for('usuarios.reset_token', token=token, _external=True)}

Si no solicitaste este cambio, simplemente ignora este correo y no se realizarán cambios.
'''
    mail.send(msg)

@bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_token(token):
    usuario = Usuario.verify_reset_password_token(token)
    if not usuario:
        flash('Token inválido o expirado.')
        return redirect(url_for('usuarios.restablecer_contraseña'))
    
    if request.method == 'POST':
        contraseña = request.form.get('contraseña')
        usuario.set_password(contraseña)
        db.session.commit()
        flash('Tu contraseña ha sido actualizada.')
        return redirect(url_for('login.login'))
    
    return render_template('auth/reset_token.html')




