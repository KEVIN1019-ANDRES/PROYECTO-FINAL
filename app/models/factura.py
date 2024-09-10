from app import db

class Factura(db.Model):
    __tablename__='factura'
    id= db.Column(db.Integer, primary_key=True,  autoincrement=True)
    fecha= db.Column(db.String(255), nullable=False)
    total= db.Column(db.String(255), nullable=False)
    usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    detalle =db.Column(db.Integer, db.ForeignKey('detalle.id'))