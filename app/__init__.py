from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager # Importar el modelo Usuario

# Inicializar SQLAlchemy y Flask-Migrate
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def formato_moneda(value):
    return f"${value:,.2f}"

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    # Configurar filtros Jinja2
    app.jinja_env.filters['formato_moneda'] = formato_moneda

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.usuario import Usuario
        return Usuario.query.get(int(user_id))

    # Importar y registrar blueprints
    from app.routes import login_routes, compra, caracteristica_routes, Carrito_routes, factura_routes, usuario_routes, Vista_routes
    app.register_blueprint(caracteristica_routes.bp)
    app.register_blueprint(compra.compra_bp)
    app.register_blueprint(Carrito_routes.bp)
    app.register_blueprint(factura_routes.bp)
    app.register_blueprint(login_routes.bp)
    app.register_blueprint(usuario_routes.bp)
    app.register_blueprint(Vista_routes.bp)


    # Importar y registrar blueprints desde admin
    from app.admin.routes import vehiculo_routes, producto_routes
    app.register_blueprint(vehiculo_routes.bp)
    app.register_blueprint(producto_routes.bp)
    
    login_manager.login_view = 'login.login'

    return app