from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)

    from app.routes import auth, employees, departments, roles
    app.register_blueprint(auth.bp)
    app.register_blueprint(employees.bp)
    app.register_blueprint(departments.bp)
    app.register_blueprint(roles.bp)

    return app