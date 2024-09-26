from app import create_app, db
from app.models.usuario import Usuario

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()

        # Verifica si ya existe un administrador
        admin = Usuario.query.filter_by(rol='admin').first()
        if not admin:
            # Crea el administrador predeterminado
            admin = Usuario(
                username='admin',
                email='admin@example.com',
                telefono='1234567890',
                rol='admin'
            )
            admin.set_password('12345')  # Establece una contraseña segura
            db.session.add(admin)
            db.session.commit()
            print("Administrador creado con éxito.")
        else:
            print("El administrador ya existe.")

if __name__ == '__main__':
    init_db()