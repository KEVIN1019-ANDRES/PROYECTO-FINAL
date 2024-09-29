from app import db

class Detalle(db.Model):
    __tablename__ = 'detalle'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    
    producto = db.relationship("Producto", back_populates="detalles")
    vehiculo = db.relationship("Vehiculo", back_populates="detalles")
    factura = db.relationship("Factura", back_populates="detalles")

    def __repr__(self):
        return f'<Detalle {self.id} del {"Producto" if self.producto_id else "Vehiculo"} {self.producto_id or self.vehiculo_id}>'
