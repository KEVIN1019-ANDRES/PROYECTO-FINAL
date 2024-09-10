from app import db

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(50), nullable=False)
    año = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    precio_anterior = db.Column(db.Integer, nullable=True)  # Precio anterior opcional
    cilindraje = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(100), nullable=True)
    
    
    detalle = db.relationship("Detalle", back_populates="vehiculo")

    def __repr__(self):
        return f'<Vehiculo {self.marca} {self.modelo}>'

    @staticmethod
    def obtener_vehiculo_por_id(id):
        return Vehiculo.query.get(id)
    
    @classmethod
    def getItems(cls):
        return cls.query.all()
