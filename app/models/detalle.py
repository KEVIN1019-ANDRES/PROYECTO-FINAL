from app import db

class Detalle(db.Model):
    __tablename__ = 'detalle'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cantidad = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.String(255), nullable=False)
    iva = db.Column(db.String(255), nullable=False)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))

    producto = db.relationship("Producto", back_populates="detalles")
    vehiculo = db.relationship("Vehiculo", back_populates="detalles")

    def __repr__(self):
        return f'<Detalle {self.id} del Vehiculo {self.vehiculo_id}>'
