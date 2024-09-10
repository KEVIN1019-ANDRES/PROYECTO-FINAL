# app/admi/routes/__init__.py
from flask import Blueprint

# Importar los Blueprints
from .producto_routes import bp as producto_bp

def register_blueprints(app):
    app.register_blueprint(producto_bp)
