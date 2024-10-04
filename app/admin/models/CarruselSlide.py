from app import db

class CarruselSlide(db.Model):
    __tablename__ = 'CarruselSlide'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    ruta = db.Column(db.String(255), nullable=True)
    orden = db.Column(db.Integer, nullable=False)
    imagen_nombre = db.Column(db.String(255), nullable=False)
    
    def __init__(self, titulo, descripcion, ruta, orden, imagen_nombre):
        self.titulo = titulo
        self.descripcion = descripcion
        self.ruta = ruta
        self.orden = orden
        self.imagen_nombre = imagen_nombre

    def __repr__(self):
        return f'<CarruselSlide {self.id}: {self.titulo}>'