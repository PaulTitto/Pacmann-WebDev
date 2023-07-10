from flask import Blueprint
from app.auth import routes

authBp = Blueprint('auth', __name__)
