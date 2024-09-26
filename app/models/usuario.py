from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    direccion = db.Column(db.String(200), nullable=True)  # Dirección opcional
    rol = db.Column(db.String(20), nullable=False, default='cliente')

    def set_password(self, password):
        from app import db  # Importar db dentro de la función
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_role(self, role):
        self.rol = role
        db.session.commit()
