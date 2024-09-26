from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario import Usuario  # Asegúrate de importar el modelo Usuario

bp = Blueprint('login', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('nombreU')
        contraseña = request.form.get('contraseña')
        
        # Busca el usuario en la base de datos
        user = Usuario.query.filter_by(username=usuario).first()
        
        # Verifica si el usuario existe y la contraseña es correcta
        if user and user.check_password(contraseña):
            # Autenticación exitosa
            session['user_id'] = user.id
            session['user_role'] = user.rol
            
            flash('Inicio de sesión exitoso', 'success')
            
            # Redirigir según el rol del usuario
            if user.rol == 'admin':
                return redirect(url_for('admin.gestionar_vehiculos'))  # Ruta para administradores
            else:
                return redirect(url_for('tienda.catalogo'))  # Ruta para usuarios normales
        else:
            flash('Credenciales inválidas', 'danger')
    
    return render_template('login/index.html')

