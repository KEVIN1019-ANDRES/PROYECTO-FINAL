from app import db
from werkzeug.security import generate_password_hash, check_password_hash
# No importamos db aquí al inicio para evitar la importación circular

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    direccion = db.Column(db.String(200), nullable=True)  # Dirección opcional
    rol = db.Column(db.String(20), nullable=True, default='cliente')

    def set_password(self, password):
        from app import db  # Importar db dentro de la función
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
