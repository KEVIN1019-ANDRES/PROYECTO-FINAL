from app import db  # Asegúrate de importar db desde el lugar correcto

class Vehiculo(db.Model):
    __tablename__ = 'vehiculo'  # Nombre de la tabla en la base de datos (opcional)
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
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    # Relación con Detalle
    detalles = db.relationship('Detalle', back_populates='vehiculo')

    def __repr__(self):
        return f'<Vehiculo {self.marca} {self.modelo}>'

    @staticmethod
    def obtener_vehiculo_por_id(id):
        return Vehiculo.query.get(id)
    
    @classmethod
    def getItems(cls):
        return cls.query.all()
