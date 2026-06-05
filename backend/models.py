from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(30), nullable=False) # Admin / Student / Company
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    student = db.relationship("Student", backref="user", uselist=False)
    company = db.relationship("Company", backref="user", uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), unique=True, nullable=False)

    name = db.Column(db.String(30), nullable=False)
    skills = db.Column(db.String(200))
    dept = db.Column(db.String(30), nullable=False)
    course = db.Column(db.String(30), nullable=False)
    cgpa = db.Column(db.Numeric(3, 2), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    backlog_count = db.Column(db.Integer, nullable=False)
    resume = db.Column(db.String(255))

    applications = db.relationship("Application", backref="student")
    notifications = db.relationship("Notification", backref="student")

class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), unique=True, nullable=False)

    name = db.Column(db.String(30), nullable=False)
    industry = db.Column(db.String(50))
    location = db.Column(db.String(150))
    website = db.Column(db.String(150))
    status = db.Column(db.String(30), nullable=False, default="Pending") # Pending / Approved / Rejected

    drives = db.relationship("Drive", backref="company")

class Drive(db.Model):
    drive_id = db.Column(db.Integer, primary_key=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'), nullable=False)
    job_title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(200))
    salary = db.Column(db.Numeric(12, 4), nullable=False)
    eligibility_cgpa = db.Column(db.Numeric(3, 2))
    eligibility_graduation_year = db.Column(db.Integer)
    eligibility_backlog_count = db.Column(db.Integer)
    required_skills = db.Column(db.String(300))
    deadline = db.Column(db.Date, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(30), nullable=False, default="Approved") # Approved / Closed / Blacklisted

    applications = db.relationship('Application', backref="drive")

class Application(db.Model):
    application_id = db.Column(db.Integer, primary_key=True, nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.drive_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    current_status = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)

    application_status = db.relationship("ApplicationStatus", backref="application")
    interviews = db.relationship("Interview", backref="application")

    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="unique_student_drive"),
    )

class ApplicationStatus(db.Model):
    application_status_id = db.Column(db.Integer, primary_key=True, nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey("application.application_id"), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="Applied") # Applied / Rejected / Selected
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)


class Notification(db.Model):
    notification_id = db.Column(db.Integer, primary_key=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    is_seen = db.Column(db.Boolean, nullable=False, default=False)
    title = db.Column(db.String(100))
    message = db.Column(db.String(300))

class Placement(db.Model):
    placement_id = db.Column(db.Integer, primary_key=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'), nullable=False)
    position = db.Column(db.String(50))
    salary = db.Column(db.Numeric(12, 4), nullable=False)
    joining_date = db.Column(db.Date)

    student = db.relationship("Student", backref="placements")
    company = db.relationship("Company", backref="placements")

class Interview(db.Model):
    interview_id = db.Column(db.Integer, primary_key=True, nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey("application.application_id"), nullable=False)
    type = db.Column(db.String(50), nullable=False) # Online / Offline
    feedback = db.Column(db.String(300))
    scheduled_at = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(300))
