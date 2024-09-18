from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario import Usuario  # Asegúrate de importar el modelo Usuario

bp = Blueprint('login', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    print("entra al login")
    if request.method == 'POST':
        usuario = request.form.get('nombreU')
        contraseña = request.form.get('contraseña')
        
        print(f"Usuario: {usuario}")
        print(f"Contraseña: {contraseña}")
        
        # Busca el usuario en la base de datos
        user = Usuario.query.filter_by(username=usuario).first()
        
        # Verifica si el usuario existe y la contraseña es correcta
        if user and user.check_password(contraseña):
            # Autenticación exitosa
            session['user_id'] = user.id  # Guardamos el id del usuario en la sesión
            session['user_role'] = user.rol  # Guardamos el rol del usuario en la sesión
            
            flash('Inicio de sesión exitoso', 'success')
            
            # Redirigir según el rol del usuario
            if user.rol == 'admin':
                return redirect(url_for('admin_dashboard'))  # Redirigir al panel de admin
            else:
                return redirect(url_for('index'))  # Redirigir al dashboard de cliente
        else:
            flash('Credenciales inválidas', 'danger')
    print("antes del login")
    return render_template('vista/index.html')
