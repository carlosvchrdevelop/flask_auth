from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'HASDFKJJH$&DSAJKHjdfhskdf823eiuhdeh'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pguser:pgpass@localhost/midatabase'

    db.init_app(app)

    # blueprint para las rutas de nuestra app que requieran autenticación
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint para las rutas de nuestra app que no requieran autenticación
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app