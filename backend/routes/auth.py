from flask import Blueprint
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

import models
from validator import *

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
auth_api = Api(auth_bp)

# User Registraion

register_parser = reqparse.RequestParser()
register_parser.add_argument("email", type=validate_email, required=True)
register_parser.add_argument("password",type=validate_password,required=True)
register_parser.add_argument("role", type=validate_role, required=True)

class User(Resource):
    def post(self):
        args = register_parser.parse_args()
        user = models.User(email=args["email"], role=args["role"])
        user.set_password(args["password"])

        if (args["role"] == "company"):
            user.is_active = False

        try:
            models.db.session.add(user)
            models.db.session.commit()
        except IntegrityError:
            models.db.session.rollback()
            return {
                "message": {
                    "email": "User with this email already exists!"
                }
            }, 409

        return {
            "message": f"{args['role'].title()} added successfully"
        }, 201
    
    @jwt_required()
    def get(self):
        
        user_id = int(get_jwt_identity())
        user = models.User.query.filter(models.User.user_id == user_id).first()
        
        if (user):

            profile_complete = True

            if user.role == "student":
                if not user.student:
                    profile_complete = False

            elif user.role == "company":
                if not user.company:
                    profile_complete = False

            return {
                "status": "success",
                "message": "user found",
                "user_id": user.user_id,
                "role": user.role,
                "profile_complete": profile_complete
            }, 200
        
        return {
            "status": "error",
            "message": "unauthorized"
        }, 401

# User Login

login_parser = reqparse.RequestParser()
login_parser.add_argument("email", type=validate_email, required=True)
login_parser.add_argument("password",type=validate_password,required=True)

class LoginUser(Resource):
    def post(self):
        args = login_parser.parse_args()
        email = args["email"]
        password = args["password"]

        user = models.User.query.filter(models.User.email == email).first()
        if not (user and user.check_password(password)):
            return {
                "status": "error",
                "message": "User email or password incorrect"
            }, 401
        
        if (user.role == "company" and not user.is_active):
            return {
                "status": "error",
                "message": "Admin approval pending"
            }
        
        access_token = create_access_token(identity=str(user.user_id))
        return {
            "status": "success",
            "message": "User loggin in successful!",
            "role": user.role,
            "id": user.user_id,
            "access_token" : access_token
        }, 200


auth_api.add_resource(User,"/users")
auth_api.add_resource(LoginUser, "/login")
