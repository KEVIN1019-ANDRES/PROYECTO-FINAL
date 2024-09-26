from flask import Blueprint, render_template, request, redirect, url_for
from app.models.factura import Factura
from app.models.detalle import Detalle
from datetime import datetime
from app import db


bp = Blueprint('factura', __name__)


@bp.route('/factura')
def index():
    data = Factura.query.all()
    
    
    return render_template('factura/index.html', factura=data)
    #return data
    

@bp.route('/addfactura', methods=['GET', 'POST'])
def add():
    nueva_factura = Factura(fechafactura=datetime.now().date(), idcliente=1)
    db.session.add(nueva_factura)
    db.session.commit()
    print("factura id ", nueva_factura.idfactura)
    return redirect(url_for('factura.addDetalle', id=nueva_factura.idfactura))



@bp.route('/delete/<int:id>')
def Delete(id):
    book = Factura.query.get_or_404(id)
    
    
    db.session.delete(book)
    db.session.commit()
    
    return redirect(url_for('factura.index'))




@bp.route('/factura/Listar/<int:id>', methods=['GET', 'POST'])
def list(id):

    author = Factura.query.get_or_404(id)
    books = author.books
    if request.method == 'POST':
        author.nombre = request.form['nombre']
        author.nacionalidad = request.form['nacionalidad']
        db.session.commit()
        return redirect(url_for('author.index'))
    #return author.nombre
    return render_template('authors/List.html', books=books)
    