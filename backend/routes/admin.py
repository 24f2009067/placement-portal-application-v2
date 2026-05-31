from flask import Blueprint
from flask_restful import Resource, Api

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")
admin_api = Api(admin_bp)