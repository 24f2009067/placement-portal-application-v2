from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
import models
import tasks
from datetime import date, datetime

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
            company = models.Company(user_id=user_id, name=name, industry=industry, location=location, website=website, status="pending")
            models.db.session.add(company)
            models.db.session.commit()

        return {
            "status": "success",
            "message": "company profile updated"
        }, 200
    
class Dashboard(Resource):

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
            search = request.args.get("search")
            drives = models.Drive.query.filter(models.Drive.company_id == company.company_id)
            applications = (
                models.Application.query
                .join(models.Drive)
                .filter(
                    models.Drive.company_id == company.company_id,
                    models.Application.current_status.in_(["selected", "shortlisted"]),
                )
            )
            
            if search:
                if search.isdigit():
                    drives = drives.filter(models.Drive.drive_id == int(search))
                    applications = applications.filter(models.Application.application_id == int(search))

                else:
                    drives = drives.filter(or_(
                            models.Drive.job_title.ilike(f"%{search}%"),
                            models.Company.name.ilike(f"%{search}%")
                            )
                        )
                    
                    applications = applications.filter(or_(
                    models.Application.current_status.ilike(f"%{search}%"),
                    models.Student.name.ilike(f"%{search}%"),
                    models.Company.name.ilike(f"%{search}%"),
                    models.Drive.job_title.ilike(f"%{search}%")
                    )
                )

            pending_drives = drives.filter(models.Drive.status == "pending")
            approved_drives = drives.filter(models.Drive.status == "approved")
            closed_drives = drives.filter(models.Drive.status == "closed")
            removed_drives = drives.filter(models.Drive.status == "removed")
            
            applications = [{
                    "status": "success",
                    "message": "applications fetched successfully",
                    "application_id": application.application_id,
                    "company_name": application.drive.company.name,
                    "job_title": application.drive.job_title,

                    "student_id": application.student.student_id,
                    "student_name": application.student.name,
                    "dept": application.student.dept,
                    "course": application.student.course,
                    "skills": application.student.skills,
                    "resume": True if application.student.resume else False,

                    "application_status": application.current_status,
                    "created_on": str(application.created_on)
                } for application in applications.all()]
            
            return{
                "status": "success",
                "message": "company dashboard data fetched!",
                "data": {
                    "pendingDrives" : makeDict(pending_drives.all()),
                    "approvedDrives" : makeDict(approved_drives.all()),
                    "closedDrives" : makeDict(closed_drives.all()),
                    "removedDrives" : makeDict(removed_drives.all()),
                    "applications": applications
                }
            }


        else:
            return {
                "status": "error",
                "message": "company profile not complete",
            }, 404

class Drive(Resource):

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
        if company:
            data = request.json
            drive = models.Drive(
                    company_id=company.company_id,
                    job_title=data.get("job_title"),
                    description=data.get("description"),
                    salary=float(data.get("salary")),
                    eligibility_cgpa=float(data.get("eligibility_cgpa")),
                    eligibility_graduation_year=int(data.get("eligibility_graduation_year")),
                    eligibility_backlog_count=int(data.get("eligibility_backlog_count")),
                    required_skills=data.get("required_skills"),
                    deadline= date.fromisoformat(data.get("deadline")),
                )
            
            try:
                models.db.session.add(drive)
                models.db.session.commit()
                return{
                    "status": "success",
                    "message": "Drive added successfully!"
                }
            except Exception as e:
                models.db.rollback()
                return {
                    "status": "error",
                    "message": "Unable to update DB"
                }, 500

        else:
            return {
                "status": "error",
                "message": "company profile not complete",
            }, 404

    @jwt_required()
    def put(self, drive_id, action):
        user_id = get_jwt_identity()
        user = models.User.query.filter(models.User.user_id == user_id).first()
        if (user == None):
            return {
                "status": "error",
                "message": "User not registered!",
            }, 404
        
        company = user.company
        if company:
            if action:
                    drive = models.Drive.query.filter(models.Drive.drive_id == drive_id).first();
                    if not drive:
                        return {
                            "status": "error",
                            "message": "invalid drive id",
                        }, 404
                    
                    if drive.company_id != company.company_id:
                        return {
                            "status": "error",
                            "message": "Forbidden operation",
                        }, 403
                    
                    if action == "close":
                        drive.status = "closed"
                        try:
                            models.db.session.commit()
                        except Exception as e:
                            models.db.rollback()
                            return {
                                "status": "error",
                                "message": "Unable to update DB"
                            }, 500
                        
                        return {
                            "status": "success",
                            "message": f"{drive.job_title}, {drive.company.name} was closed"
                        }, 200
                    
                    if action == "update":
                        data = request.json
                        drive.job_title = data['job_title']
                        drive.description = data['description']
                        drive.salary = data['salary']
                        drive.eligibility_cgpa = data['eligibility_cgpa']
                        drive.eligibility_graduation_year = data['eligibility_graduation_year']
                        drive.eligibility_backlog_count = data['eligibility_backlog_count']
                        drive.required_skills = data['required_skills']
                        drive.deadline = date.fromisoformat(data['deadline'])

                        drive.status = "pending"
                        try:
                            models.db.session.commit()
                        except Exception as e:
                            models.db.rollback()
                            return {
                                "status": "error",
                                "message": "Unable to update DB"
                            }, 500
                        
                        return {
                            "status": "success",
                            "message": f"{drive.job_title}, {drive.company.name} was updated"
                        }, 200

        else:
            return {
                "status": "error",
                "message": "company profile not complete",
            }, 404
        
    @jwt_required()
    def get(self, drive_id):
        user_id = get_jwt_identity()
        user = models.User.query.filter(models.User.user_id == user_id).first()
        if (user == None):
            return {
                "status": "error",
                "message": "User not registered!",
            }, 404
        
        company = user.company
        if company:
            drive = models.Drive.query.filter(models.Drive.drive_id == drive_id).first()
            if not drive or drive.company_id != company.company_id:
                return {
                    "status": "error",
                    "message": "You are not authorized to access this drive."
                }, 403
            
            applications = [{
                "application_id": application.application_id,
                "company_name": application.drive.company.name,
                "job_title": application.drive.job_title,

                "student_id": application.student.student_id,
                "student_name": application.student.name,
                "dept": application.student.dept,
                "course": application.student.course,
                "skills": application.student.skills,
                "resume": True if application.student.resume else False,

                "application_status": application.current_status,
                "created_on": str(application.created_on)
            } for application in drive.applications]
                        
            return {
                    "status": "success",
                    "message": "drive fetched",
                    "job_title": drive.job_title,
                    "description": drive.description,
                    "salary": str(drive.salary),
                    "eligibility_cgpa": str(drive.eligibility_cgpa),
                    "eligibility_graduation_year": str(drive.eligibility_graduation_year),
                    "eligibility_backlog_count": str(drive.eligibility_backlog_count),
                    "required_skills": drive.required_skills,
                    "deadline": drive.deadline.isoformat(),
                    "applications": applications
            }, 200
        else:
            return {
                "status": "error",
                "message": "company profile not complete",
            }, 404

class Application(Resource):

    @jwt_required()
    def put(self, application_id, status):
        user_id = get_jwt_identity()
        user = models.User.query.filter(models.User.user_id == user_id).first()
        if (user == None):
            return {
                "status": "error",
                "message": "User not registered!",
            }, 404
        
        company = user.company
        if company:
            if status and status in ["select", "shortlist", "reject"]:
                application = models.Application.query.filter(models.Application.application_id == application_id).first()
                if application:
                    
                    if status == "select":
                        application.current_status = "selected"
                        application_status = models.ApplicationStatus(application_id=application_id, status="selected")
                        placement = models.Placement(
                            student_id = application.student.student_id,
                            company_id = application.drive.company.company_id,
                            position = request.json.get("position"),
                            salary = request.json.get("salary"),
                            joining_date = date.fromisoformat(request.json.get("joining_date"))
                        )
                        notification = models.Notification(
                            student_id=application.student.student_id,
                            title= f"{application.drive.company.name} • {application.drive.job_title}",
                            message = f"Your application has been selected."             
                        )
                        models.db.session.add(notification)
                        models.db.session.add(application_status)
                        models.db.session.add(placement)

                    elif status == "shortlist":
                        application.current_status = "shortlisted"
                        application_status = models.ApplicationStatus(application_id=application_id, status="shortlisted")
                        interview = models.Interview(
                            application_id=application_id,
                            type = request.json.get(("mode")),
                            feedback = request.json.get(("feedback")),
                            location = request.json.get(("location")),
                            scheduled_at = datetime.fromisoformat(request.json.get(("scheduled_at"))),
                        )
                        notification = models.Notification(
                            student_id=application.student.student_id,
                            title= f"{application.drive.company.name} • {application.drive.job_title}",
                            message = f"Your application has been shortlisted."             
                        )
                        models.db.session.add(notification)
                        models.db.session.add(application_status)
                        models.db.session.add(interview)

                    elif status == "reject":
                        application.current_status = "rejected"
                        application_status = models.ApplicationStatus(application_id=application_id, status="rejected")
                        models.db.session.add(application_status)
                        notification = models.Notification(
                            student_id=application.student.student_id,
                            title= f"{application.drive.company.name} • {application.drive.job_title}",
                            message = f"Your application has been rejected."             
                        )
                        models.db.session.add(notification)
                    try:
                        models.db.session.commit()
                        return {
                            "status": "success",
                            "message": "application updated successfully"
                        }, 200
                    
                    except Exception as e:
                        models.db.session.rollback()
                        return {
                            "status": "error",
                            "message": "Error updating db"
                        }, 500

                else:
                    return {
                        "status": "error",
                        "message": "application not found",
                    }, 400
            else:
                return {
                    "status": "error",
                    "message": "missing or invalid status",
                }, 400

        else:
            return {
                "status": "error",
                "message": "company profile not complete",
            }, 404
        
class Report(Resource):

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
        if company:
            tasks.generateCompanyReport.delay(company.company_id)
            return 200
    
        else:
            return {
                "status": "error",
                "message": "company profile not complete",
            }, 404
    


company_api.add_resource(Company, "")
company_api.add_resource(Dashboard, "/dashboard")
company_api.add_resource(Drive, "/drives/<int:drive_id>/<string:action>", "/drives", "/drives/<int:drive_id>")
company_api.add_resource(Application, "/applications/<int:application_id>/<string:status>")
company_api.add_resource(Report, "/report")

# utitlities

def makeDict(drives):
    return [{
        "drive_id": drive.drive_id,
        "job_title": drive.job_title,
        "description": drive.description,
        "salary": str(drive.salary),
        "deadline": str(drive.deadline),
        "drive_status": drive.status,

        "eligibility_cgpa": str(drive.eligibility_cgpa),
        "eligibility_graduation_year": drive.eligibility_graduation_year,
        "eligibility_backlog_count": drive.eligibility_backlog_count,
        "required_skills": drive.required_skills,

        "company_name": drive.company.name,
    } for drive in drives]

