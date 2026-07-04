from flask import Blueprint, request
from flask_restful import Resource, Api
import models
from sqlalchemy import or_
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")
admin_api = Api(admin_bp)
    
class Companies(Resource):

    @jwt_required()
    def get(self):
        verifyRole()
        args = request.args
        status = args.get("status")
        search = args.get("search")

        query = models.Company.query.join(models.User)

        if status:
            if status == "pending":
                query = query.filter(
                    models.Company.status == "pending"
                )

            elif status == "approved":
                query = query.filter(
                    models.Company.status == "approved"
                )

            elif status == "removed":
                query = query.filter(
                    models.Company.status == "removed"
                )

        if search:
            query = query.filter(
                or_(
                    models.User.email.ilike(f"%{search}%"),
                    models.Company.name.ilike(f"%{search}%"),
                    models.Company.industry.ilike(f"%{search}%")
                )
            )

        companies = query.all()

        comp_list = [{
            "user_id": c.user.user_id,
            "email": c.user.email,
            "name": c.name,
            "industry": c.industry,
            "status": c.status
        } for c in companies]

        return {
            "status": "success",
            "message": f"{status} companies fetched successfully",
            "companies": comp_list
        }, 200
    
    @jwt_required()
    def put(self, user_id):
        verifyRole()
        
        user = models.User.query.filter(models.User.user_id == user_id).first()
        company = user.company
        if user and user.role == "company" and company:

            if company.status == "approved":
                return 200

            try:
                company.status = "approved"
                user.is_active = True
                models.db.session.commit()

                return {
                    "status": "success",
                    "message": f"{company.name} was approved"
                }, 200
            except Exception as e:
                return {
                    "status": "error",
                    "message": "Unable to update DB"
                }, 500
        else:
            models.db.rollback()
            return {
                "status": "error",
                "message": "user not found"
            }, 404
        
    @jwt_required()
    def delete(self, user_id):
        verifyRole()
        
        user = models.User.query.filter(models.User.user_id == user_id).first()
        company = user.company
        if user and user.role == "company" and company:

            if company.status == "removed":
                return 200
            try:
                company.status = "removed"
                for drive in company.drives:
                    drive.status = "removed"
                    for application in drive.applications:
                        application.current_status = "company_removed"
                        application_status = models.ApplicationStatus(application_id=application.application_id, status="company_removed")
                        notification = models.Notification(
                            student_id=application.student.student_id,
                            title= f"{application.drive.company.name} • {application.drive.job_title}",
                            message = f"The company {application.drive.company.name} was blacklisted by the admin."             
                        )
                        models.db.session.add(notification)
                        models.db.session.add(application_status)
                models.db.session.commit()
                return {
                    "status": "success",
                    "message": f"{company.name} was Blacklisted"
                }, 200
            except Exception as e:
                return {
                    "status": "error",
                    "message": "Unable to update DB"
                }, 500
        else:
            models.db.rollback()
            return {
                "status": "error",
                "message": "user not found"
            }, 404

class Students(Resource):

    @jwt_required()
    def get(self):
        verifyRole()

        status = request.args.get("status")
        search = request.args.get("search")

        students = models.Student.query.join(models.User)

        if status:
            if status == "approved":
                students = students.filter(models.User.is_active == True)

            elif status == "removed":
                students = students.filter(models.User.is_active == False)

        if search:
            if search.isdigit():
                students = students.filter(models.User.user_id == int(search))

            else:
                students = students.filter(or_(
                    models.User.email.ilike(f"%{search}%"),
                    models.Student.name.ilike(f"%{search}%")
                    )
                )

        student_list = [{
            "user_id": s.user.user_id,
            "email": s.user.email,
            "name": s.name,
            # "skills": s.skills,
            # "dept": s.dept,
            # "course": s.course,
            # "cgpa": str(s.cgpa),
            # "graduation_year": str(s.graduation_year),
            # "backlog_count": str(s.backlog_count)
        } for s in students.all()]

        return {
            "status": "success",
            "message": "students fetched successfully",
            "students": student_list
        }, 200
    
    @jwt_required()
    def delete(self, user_id):
        verifyRole()
        
        user = models.User.query.filter(models.User.user_id == user_id).first()
        student = user.student
        if user and user.role == "student" and student:

            if user.is_active == False:
                return 200
            
            try:
                user.is_active = False
                for application in student.applications:
                    application.current_status = "student_removed"
                    application_status = models.ApplicationStatus(application_id=application.application_id, status="student_removed")
                    notification = models.Notification(
                        student_id=application.student.student_id,
                        title= f"{application.drive.company.name} • {application.drive.job_title}",
                        message = f"You were blacklisted by the admin."             
                    )
                    models.db.session.add(notification)
                    models.db.session.add(application_status)


                models.db.session.commit()
                return {
                    "status": "success",
                    "message": f"{student.name} was Blacklisted"
                }, 200
            except Exception as e:
                return {
                    "status": "error",
                    "message": "Unable to update DB"
                }, 500
        else:
            models.db.rollback()
            return {
                "status": "error",
                "message": "user not found"
            }, 404
    
class Applications(Resource):

    @jwt_required()
    def get(self, application_id=None):
        verifyRole()

        if application_id is not None:
            application = models.Application.query.filter(models.Application.application_id == application_id).first()

            if application:
                return {
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
                }, 200
            else:
                return {
                    "status": "error",
                    "message": "Application not found"
                }, 404

        search = request.args.get("search")

        applications = models.Application.query.join(models.Drive).join(models.Student).join(models.Company)

        if search:
            if search.isdigit():
                applications = applications.filter(models.Application.application_id == int(search))

            else:
               applications = applications.filter(or_(
                    models.Student.name.ilike(f"%{search}%"),
                    models.Company.name.ilike(f"%{search}%"),
                    models.Drive.job_title.ilike(f"%{search}%"),
                    models.Application.current_status.ilike(f"%{search}%")
                    )
                )
            
        application_list = [{
            "application_id": a.application_id,
            "company_name": a.drive.company.name,
            "student_name": a.student.name,
            "job_title": a.drive.job_title,
            "status": a.current_status
        } for a in applications.all()]

        return {
            "status": "success",
            "message": "applications fetched successfully",
            "applications": application_list
        }, 200
    
class Drives(Resource):

    @jwt_required()
    def get(self, drive_id=None):
        verifyRole()

        if drive_id is not None:
            drive = models.Drive.query.filter(models.Drive.drive_id == drive_id).first()

            if drive:
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

                    "company_name": drive.company.name,


                }, 200
            else:
                return {
                    "status": "error",
                    "message": "Drive not found"
                }, 404


        status = request.args.get("status")
        search = request.args.get("search")

        drives = models.Drive.query.join(models.Company)

        if status:
            if status == "pending":
                drives = drives.filter(models.Drive.status == "pending")

            elif status == "approved":
                drives = drives.filter(models.Drive.status == "approved")

            elif status == "closed":
                drives = drives.filter(models.Drive.status == "closed")

            elif status == "removed":
                drives = drives.filter(models.Drive.status == "removed")
        
        if search:
            if search.isdigit():
                drives = drives.filter(models.Drive.drive_id == int(search))

            else:
               drives = drives.filter(or_(
                    models.Drive.job_title.ilike(f"%{search}%"),
                    models.Company.name.ilike(f"%{search}%")
                    )
                )
               
        drive_list = [{
            "drive_id": d.drive_id,
            "company_name": d.company.name,
            "job_title": d.job_title,
            "deadline": str(d.deadline)
        } for d in drives.all()]

        return {
            "status": "success",
            "message": "drives fetched successfully",
            "drives": drive_list
        }, 200
    
    @jwt_required()
    def delete(self, drive_id, op):
        verifyRole()
        
        drive = models.Drive.query.filter(models.Drive.drive_id == drive_id).first()
        if drive:

            if drive.status == "removed":
                return 200
            
            try:
                drive.status = "removed"
                for application in drive.applications:
                    application.current_status = "drive_removed"
                    application_status = models.ApplicationStatus(application_id=application.application_id, status="drive_removed")
                    notification = models.Notification(
                        student_id=application.student.student_id,
                        title= f"{application.drive.company.name} • {application.drive.job_title}",
                        message = f"The drive {application.drive.job_title}, {application.drive.company.name} was blacklisted by the admin."             
                    )
                    models.db.session.add(notification)
                    models.db.session.add(application_status)


                models.db.session.commit()
                return {
                    "status": "success",
                    "message": f"{drive.job_title}, {drive.company.name} was Blacklisted"
                }, 200
            except Exception as e:
                return {
                    "status": "error",
                    "message": "Unable to update DB"
                }, 500
        else:
            models.db.rollback()
            return {
                "status": "error",
                "message": "drive not found"
            }, 404
        
    @jwt_required()
    def put(self, drive_id, op):
        verifyRole()
        
        drive = models.Drive.query.filter(models.Drive.drive_id == drive_id).first()
        if drive:
            
            try:
                if op == "approve":
                    if drive.status == "approve": return 200
                    drive.status = "approved"
                    models.db.session.commit()
                
                elif op == "close":
                    if drive.status == "closed": return 200
                    drive.status = "closed"
                    models.db.session.commit()

                else:
                    return {
                        "status": "error",
                        "message": "Operation not specified"
                    }, 400

                return {
                    "status": "success",
                    "message": f"{drive.job_title}, {drive.company.name} was {op}d"
                }, 200
            except Exception as e:
                return {
                    "status": "error",
                    "message": "Unable to update DB"
                }, 500
        else:
            models.db.rollback()
            return {
                "status": "error",
                "message": "drive not found"
            }, 404


admin_api.add_resource(Companies, "/companies", "/companies/<int:user_id>/approve", "/companies/<int:user_id>/remove")
admin_api.add_resource(Students, "/students", "/students/<int:user_id>/remove")
admin_api.add_resource(Applications, "/applications", "/applications/<int:application_id>")
admin_api.add_resource(Drives, "/drives", "/drives/<int:drive_id>/<string:op>", "/drives/<int:drive_id>")

# utility
def verifyRole():
    user_id = int(get_jwt_identity())
    user = models.User.query.filter(models.User.user_id == user_id).first()
    if not user or user.role != "admin":
        return {
            "status": "error",
            "message": "unauthorized"
        }, 401