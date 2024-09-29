from app import db
from datetime import datetime

class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    metodo_entrega = db.Column(db.String(50))
    total = db.Column(db.Float)
    departamento = db.Column(db.String(100))
    municipio = db.Column(db.String(100))
    metodo_pago = db.Column(db.String(50))

    usuario = db.relationship('Usuario', back_populates='facturas')
    detalles = db.relationship('Detalle', back_populates='factura', lazy='dynamic')

    def __repr__(self):
        return f'<Factura {self.id} del Usuario {self.usuario_id}>'