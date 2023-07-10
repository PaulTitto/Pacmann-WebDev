from flask import Blueprint
from app.user import routes

userBp = Blueprint('user', __name__)