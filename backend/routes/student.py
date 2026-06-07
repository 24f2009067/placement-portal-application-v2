from flask import Blueprint, request, send_file
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
import models
import uuid
import os

student_bp = Blueprint("student", __name__, url_prefix="/api/students")
student_api = Api(student_bp)

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
        
        if (student.resume):
            return send_file(student.resume)
        else:
            return {
                "status": "error",
                "message": "No files found!"
            }, 404
    
    return {
        "status": "error",
        "message": "student not found"
    }, 404


student_api.add_resource(Student, "/")