from flask import render_template, redirect, url_for, request
from app import app, db
from app.forms.registro_form import RegistroForm
from app.models.usuario import Usuario

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistroForm()
    if form.validate_on_submit():
        usuario = Usuario(
            username=form.username.data,
            email=form.email.data,
            telefono=form.telefono.data,
            password=form.password.data  # Asegúrate de cifrar la contraseña antes de guardarla
        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
