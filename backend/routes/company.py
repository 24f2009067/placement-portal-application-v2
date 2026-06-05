from flask import Blueprint
from flask_restful import Resource, Api

company_bp = Blueprint("company", __name__, url_prefix="/api/company")
company_api = Api(company_bp)

