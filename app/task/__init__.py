from flask import Blueprint
from app.task import routes

taskBp = Blueprint('task', __name__)