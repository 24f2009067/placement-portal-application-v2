from flask import Blueprint
from flask_restful import Resource, Api

student_bp = Blueprint("student", __name__, url_prefix="/api/student")
student_api = Api(student_bp)

