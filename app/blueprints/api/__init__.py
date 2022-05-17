from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix='/api')

from .import reading_routes, auth_routes, models