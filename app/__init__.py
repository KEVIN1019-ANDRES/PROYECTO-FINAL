from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()  # Inicialización de SQLAlchemy
migrate = Migrate()
mail=Mail()
def formato_moneda(value):
    return f"${value:,.2f}"

def create_app():
    app = Flask(__name__)
    
    # Configurar la URI de la base de datos
    app.config.from_object('config.Config')
    
    mail.init_app(app)
    # Configurar filtros Jinja2
    app.jinja_env.filters['formato_moneda'] = formato_moneda

    db.init_app(app)
    migrate.init_app(app, db)

    # Configurar filtros Jinja2
    app.jinja_env.filters['formato_moneda'] = formato_moneda

    # Importar y registrar blueprints, ahora después de inicializar db
    from app.routes import login_routes, caracteristica_routes, Carrito_routes, factura_routes, usuario_routes, Vista_routes
    
    app.register_blueprint(login_routes.auth_bp)
    app.register_blueprint(caracteristica_routes.bp)
    app.register_blueprint(Carrito_routes.bp)
    app.register_blueprint(factura_routes.bp)
    app.register_blueprint(usuario_routes.bp)
    app.register_blueprint(Vista_routes.bp)
    
    # Registrar blueprint de compra
    from app.routes import compra
    app.register_blueprint(compra.compra_bp)

    # Registrar blueprints del admin
    from app.admin.routes import vehiculo_routes, producto_routes
    app.register_blueprint(vehiculo_routes.bp)
    app.register_blueprint(producto_routes.bp)

    return app
