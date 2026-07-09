from flask import Blueprint, request, send_file
from flask_restful import Resource, Api
from sqlalchemy import or_
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
import models
import uuid
import os
from datetime import datetime

student_bp = Blueprint("student", __name__, url_prefix="/api/students")
student_api = Api(student_bp)

# utility
def verifyRole(fun):

    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = models.User.query.filter(models.User.user_id == user_id).first()
        if (user == None):
            return {
                "status": "error",
                "message": "User not registered!",
            }, 404
        
        student = user.student
        if student:
            return fun(*args, student, **kwargs)

        else:
            return {
                "status": "error",
                "message": "student profile not complete",
            }, 404

    return wrapper

def checkEligibility(student, drive):
    return student.cgpa >= drive.eligibility_cgpa and student.graduation_year <= drive.eligibility_graduation_year and student.backlog_count <= drive.eligibility_backlog_count

class Student(Resource):

# Get student profile
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = models.User.query.filter(models.User.user_id == user_id).first()
        if (user == None):
            return {
                "status": "error",
                "message": "User not registered!",
            }, 404
        
        student = user.student
        if (student):
            return {
                "status": "success",
                "profile_complete": True,
                "profile": {
                    "email": user.email,
                    "student_id": student.student_id,
                    "name": student.name,
                    "skills": student.skills,
                    "dept": student.dept,
                    "course": student.course,
                    "cgpa": str(student.cgpa),
                    "graduation_year": student.graduation_year,
                    "backlog_count": student.backlog_count,
                    "resume": student.resume
                }
            }, 200
        
        return {
            "status": "success",
            "email": user.email,
            "profile_complete": False,
            "message": "student profile incomplete"
        }, 200
    
# Create student profile
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = models.User.query.filter(models.User.user_id == user_id).first()
        if (user == None):
            return {
                "status": "error",
                "message": "User not registered!",
            }, 404

        form = request.form
        files = request.files

        name = form["name"]
        skills = form["skills"]
        dept = form["dept"]
        course = form["course"]
        cgpa = float(form["cgpa"])
        graduation_year = form["graduation_year"]
        backlog_count = form["backlog_count"]
        resume_added = False if form["resume_added"] == "false" else True

        if resume_added:
            resume = files.get("resume")
            filename = (str(uuid.uuid4()) + ".pdf")
            filepath = f"uploads/{filename}"
            os.makedirs("uploads", exist_ok=True)
            resume.save(filepath)
        else:
            filepath = ""
        

        student = user.student
        if student:
            student.name = name
            student.skills = skills
            student.dept = dept
            student.course = course
            student.cgpa = cgpa
            student.graduation_year = graduation_year
            student.backlog_count = backlog_count

            if student.resume:
                if os.path.exists(student.resume):
                    os.remove(student.resume)

            student.resume = filepath
            models.db.session.commit()
        
        else:
            student = models.Student(
                user_id=user_id,
                name=name,
                skills=skills,
                dept=dept,
                course=course,
                cgpa=cgpa,
                graduation_year=graduation_year,
                backlog_count=backlog_count,
                resume=filepath
            )

            models.db.session.add(student)
            models.db.session.commit()

        return {
            "status": "success",
            "message": "student profile updated"
        }, 200


@student_bp.route("/resume/<int:id>")
def get_resume(id):

    student = models.Student.query.get(id)
    if student:
        try:
            if (student.resume):
                return send_file(student.resume)
            else:
                return {
                    "status": "error",
                    "message": "No files found!"
                }, 404
        except Exception as e:
                return "<h1>No Resume found at location!</h1>"
    
    return {
        "status": "error",
        "message": "student not found"
    }, 404

class Dashboard(Resource):

    @jwt_required()
    @verifyRole
    def get(self, student):
        search = request.args.get("search")

        companies = models.Company.query.join(models.User).filter(models.Company.status == "approved")
        applications = models.Application.query.join(models.Drive).join(models.Student).join(models.Company).filter(models.Student.student_id == student.student_id)

        if search:
            if search.isdigit():
                companies = companies.filter(models.Company.company_id == int(search))
                applications = applications.filter(models.Student.student_id == int(search))

            else:
                companies = companies.filter(
                    or_(
                        models.User.email.ilike(f"%{search}%"),
                        models.Company.name.ilike(f"%{search}%"),
                        models.Company.industry.ilike(f"%{search}%"),
                        models.Company.location.ilike(f"%{search}%")
                    )
                )
                applications = applications.filter(or_(
                    models.Student.name.ilike(f"%{search}%"),
                    models.Company.name.ilike(f"%{search}%"),
                    models.Drive.job_title.ilike(f"%{search}%"),
                    models.Application.current_status.ilike(f"%{search}%")
                    )
                )

        companies = [{
            "user_id": c.user.user_id,
            "name": c.name,
            "email": c.user.email,
            "industry": c.industry,
            "location": c.location,
            "website": c.website
        } for c in companies.all()]

        applications = [{
            "application_id": a.application_id,
            "company_name": a.drive.company.name,
            "job_title": a.drive.job_title,
            "created_on": datetime.isoformat(a.created_on),
            "status": a.current_status
        } for a in applications.all()]

        return {
            "status": "success",
            "message": "Student dashboard fetch successfully",
            "data": {
                "companies": companies,
                "applications": applications
            }
        }, 200
    
class Company(Resource):

    @jwt_required()
    @verifyRole
    def get(self, student, user_id):
        user = models.User.query.filter(models.User.user_id == user_id).first()
        if (user == None):
            return {
                "status": "error",
                "message": "Invalid user ID!",
            }, 404
        
        company = user.company
        if company and company.status == "approved":
            drives = models.Drive.query.join(models.Company).filter(
                models.Company.company_id == company.company_id,
                models.Drive.status == "approved"
            )

            drives = [{
                "drive_id": d.drive_id,
                "company_name": d.company.name,
                "job_title": d.job_title,
                "deadline": str(d.deadline)
            } for d in drives.all()]

            return {
                "status": "success",
                "message": "company data fetched successfully!",
                "company_name": company.name,
                "company_email": company.user.email,
                "drives": drives
            }
        else:
            return {
                "status": "error",
                "message": "You don't have permission to view this page!",
            }, 404
            
class Drives(Resource):

    @jwt_required()
    @verifyRole
    def get(self, student, drive_id=None):

        if drive_id is not None:
            drive = models.Drive.query.filter(models.Drive.drive_id == drive_id).first()

            if drive:

                eligible = checkEligibility(student, drive)

                return {
                    "status": "success",
                    "message": "drive fetched successfully",

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
                    "eligible": eligible,

                    "company_name": drive.company.name,


                }, 200
            else:
                return {
                    "status": "error",
                    "message": "Drive not found"
                }, 404
        else:
            return {
                "status": "error",
                "message": "Invalid Drive ID!"
            }, 400
        
class Application(Resource):

    @jwt_required()
    @verifyRole
    def post(self, student, drive_id):
        if drive_id:
            drive = models.Drive.query.filter(models.Drive.drive_id == drive_id).first()
            if drive:
                eligible = checkEligibility(student, drive)
                if eligible:
                    application = models.Application(
                        drive_id = drive.drive_id,
                        student_id = student.student_id,
                    )


                    try:
                        models.db.session.add(application)
                        models.db.session.flush()

                        application_status = models.ApplicationStatus(
                            application_id = application.application_id,
                        )

                        models.db.session.add(application_status)
                        models.db.session.commit()

                        return {
                            "status" : "success",
                            "message": "Application sent successfully!"
                        }, 200

                    except IntegrityError as e:
                        models.db.session.rollback()
                        print(e)
                        return {
                            "status": "error",
                            "message": "Application already exists!"
                        }, 409
                    
                    except Exception as e:
                        models.db.session.rollback()
                        return {
                            "status": "error",
                            "message": "Error updating the DB!"
                        }, 500
                else:
                    return {
                        "status": "success",
                        "message": "You are not eligible to apply for this drive."
                    }, 200
            else:
                return {
                    "status": "error",
                    "message": "Drive not found"
                }, 404
        else:
            return {
                "status": "error",
                "message": "Invalid Drive ID"
            }, 400

class Notifications(Resource):

    @jwt_required()
    @verifyRole
    def get(self, student):
        notifications = models.Notification.query.filter(
            models.Notification.student_id == student.student_id,
            models.Notification.is_seen == False
        ).order_by(models.Notification.created_on.desc()).all()

        notifications = [{
            "notification_id": n.notification_id,
            "title": n.title,
            "message": n.message,
            "created_on": datetime.isoformat(n.created_on)
        } for n in notifications]

        return {
            "status": "success",
            "message": "notifications fetched",
            "notifications": notifications
        }, 200
    
    @jwt_required()
    @verifyRole
    def put(self, student, notification_id):
        if notification_id:
            notification = models.Notification.query.filter(models.Notification.notification_id == notification_id).first()
            if notification:
                notification.is_seen = True

                try:
                    models.db.session.commit()
                    return{
                        "status": "success",
                        "message": "Notification marked as read."
                    }
                except Exception as e:
                    return {
                        "status": "error",
                        "message": "Unable to update DB",
                    }, 500
            else:
                return {
                    "status": "error",
                    "message": "notification not found!",
                }, 404
          
        else:
            return {
                "status": "error",
                "message": "Invalid notification id",
            }, 400
        
class History(Resource):

    @jwt_required()
    @verifyRole
    def get(self, student):
        applications_list = []

        applications = student.applications
        for application in applications:
            interviews = [{
                "interview_id": i.interview_id,
                "type": i.type,
                "feedback": i.feedback,
                "scheduled_at": datetime.isoformat(i.scheduled_at),
                "location": i.location
            } for i in application.interviews]

            placement = models.Placement.query.join(models.Student).join(models.Company).filter(
                models.Company.company_id == application.drive.company_id,
                models.Student.student_id == application.student_id
            ).first()

            placements = []
            if placement:
                placements.append({
                    "placement_id": placement.placement_id,
                    "position": placement.position,
                    "salary" : str(placement.salary),
                    "joining_date": placement.joining_date.isoformat()
                })

            application_history = []
            for app_history in application.application_status:
                application_history.append({
                    "application_history_id": app_history.application_status_id,
                    "status": app_history.status,
                    "created_on": datetime.isoformat(app_history.created_on)
                })

            applications_list.append({
                "application_id": application.application_id,
                "company_name": application.drive.company.name,
                "job_title": application.drive.job_title,
                "interviews": interviews,
                "placements" : placements,
                "application_history": application_history
            })

        return {
            "status": "success",
            "message": "History data fetched.",
            "applications": applications_list
        }, 200
    


student_api.add_resource(Student, "")
student_api.add_resource(Company, "/company/<int:user_id>")
student_api.add_resource(Drives, "/drives/<int:drive_id>")
student_api.add_resource(Application, "/drives/<int:drive_id>/applications")
student_api.add_resource(Notifications, "/notifications", "/notifications/<int:notification_id>/seen")
student_api.add_resource(History, "/history")
student_api.add_resource(Dashboard, "/dashboard")