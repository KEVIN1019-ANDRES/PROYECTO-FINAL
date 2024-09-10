from flask import Blueprint, render_template, request, redirect, url_for, flash
from  app.models.usuario import Usuario  #Asegúrate de tener un modelo `Usuario` definido
from app import db  # Asegúrate de que `db` esté bien configurado

usuario_routes = Blueprint('usuario_routes', __name__)

@usuario_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        nombreu = request.form.get('nombreU')
        contraseña = request.form.get('contraseña')
        
        # Aquí puedes agregar lógica para verificar y guardar el nuevo usuario
        new_user = Usuario(nombre=nombre, correo=correo, telefono=telefono, nombreu=nombreu, contraseña=contraseña)
        db.session.add(new_user)
        db.session.commit()
        flash('Registro exitoso')
        return redirect(url_for('login'))  # Redirige a la página de inicio de sesión después de registrarse
    return render_template('login.html')
