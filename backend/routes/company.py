from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import models

company_bp = Blueprint("company", __name__, url_prefix="/api/company")
company_api = Api(company_bp)

company_parser = reqparse.RequestParser()
company_parser.add_argument("name", type=str, required=True)
company_parser.add_argument("industry", type=str, required=True)
company_parser.add_argument("location", type=str, required=True)
company_parser.add_argument("website", type=str, required=True)

class Company(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = models.User.query.filter(models.User.user_id == user_id).first()
        if (user == None):
            return {
                "status": "error",
                "message": "User not registered!",
            }, 404
        
        company = user.company
        if company:
            return{
                "status": "success",
                "profile_complete": True,
                "profile": {
                    "email": user.email,
                    "name": company.name,
                    "industry": company.industry,
                    "location": company.location,
                    "website": company.website
                }
            }, 200
        
        return {
            "Status": "success",
            "email": user.email,
            "profile_complete": False,
            "message": "company profile incomplete"
        }, 200
    

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = models.User.query.filter(models.User.user_id == user_id).first()
        if (user == None):
            return {
                "status": "error",
                "message": "User not registered!",
            }, 404
        
        company = user.company

        args = company_parser.parse_args()
        name = args["name"]
        industry = args["industry"]
        location = args["location"]
        website = args["website"]

        if company:
            company.name = name
            company.industry = industry
            company.location = location
            company.webste = website

            models.db.session.commit()

        else:
            company = models.Company(user_id=user_id, name=name, industry=industry, location=location, website=website, status="Approved")
            models.db.session.add(company)
            models.db.session.commit()

        return {
            "status": "success",
            "message": "company profile updated"
        }, 200



company_api.add_resource(Company, "/")