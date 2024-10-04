from app import db

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)  # Cambiado a Float para manejar decimales
    stock = db.Column(db.Integer, nullable=False)
    accesorios = db.Column(db.Integer, nullable=False)
    producto_imagen = db.Column(db.String(100), nullable=True)

    # Relación con Detalle
    detalles = db.relationship("Detalle", back_populates="producto")
