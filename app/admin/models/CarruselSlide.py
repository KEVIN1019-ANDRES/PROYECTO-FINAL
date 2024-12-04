from app import db

class CarruselSlide(db.Model):
    __tablename__ = 'CarruselSlide'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    ruta = db.Column(db.String(255), nullable=True)
    orden = db.Column(db.Integer, nullable=False)
    imagen_nombre = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(10), nullable=False)  # Añadido: categoría puede ser 'producto' o 'vehiculo'
    
    def __init__(self, titulo, descripcion, ruta, orden, imagen_nombre, categoria):
        self.titulo = titulo
        self.descripcion = descripcion
        self.ruta = ruta
        self.orden = orden
        self.imagen_nombre = imagen_nombre
        self.categoria = categoria

    def __repr__(self):
        return f'<CarruselSlide {self.id}: {self.titulo}>'