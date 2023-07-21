from flask import Flask
from config import Config
from app.extensions import db, migrate, jwt

# import blueprint
from app.task import taskBp
from app.user import userBp
from app.auth import authBp
from app.frontend import frontendBp
from app.project import projectBp

def create_app(config_class = Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    jwt.init_app(app)

    app.register_blueprint(taskBp, url_prefix='/api/tasks')
    app.register_blueprint(userBp, url_prefix='/api/users')
    app.register_blueprint(projectBp, url_prefix='/api/projects')
    app.register_blueprint(authBp, url_prefix='/api/auth')
    app.register_blueprint(frontendBp, url_prefix = "/")

    return app