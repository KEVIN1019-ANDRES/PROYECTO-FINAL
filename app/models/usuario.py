from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    direccion = db.Column(db.String(200), nullable=True)  # Dirección opcional
    rol = db.Column(db.String(20), nullable=True, default='cliente')
