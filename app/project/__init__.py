from flask import Blueprint

projectBp = Blueprint('project', __name__)

from app.project import routes