from datetime import datetime, date, timedelta

from app import app
from extensions import db
from models import (
    User,
    Student,
    Company,
    Drive,
    Application,
    ApplicationStatus,
    Notification,
    Placement,
    Interview
)


def create_user(email, password, role, is_active=True):
    user = User(
        email=email,
        role=role,
        is_active=is_active
    )
    user.set_password(password)
    return user


with app.app_context():

    # Clear existing data (child -> parent order)
    Interview.query.delete()
    ApplicationStatus.query.delete()
    Notification.query.delete()
    Placement.query.delete()
    Application.query.delete()
    Drive.query.delete()
    Company.query.delete()
    Student.query.delete()
    User.query.delete()

    db.session.commit()

    # ==================================================
    # USERS
    # ==================================================

    student_users = [
        create_user("arjun@student.com", "password", "student"),
        create_user("priya@student.com", "password", "student"),
        create_user("rahul@student.com", "password", "student"),
        create_user("ananya@student.com", "password", "student"),
        create_user("vikram@student.com", "password", "student"),
        create_user("neha@student.com", "password", "student"),
        create_user("harshith@student.com", "password", "student", False),
    ]

    company_users = [
        create_user("hr@tcs.com", "password", "company"),
        create_user("hr@infosys.com", "password", "company"),
        create_user("hr@wipro.com", "password", "company"),
        create_user("hr@accenture.com", "password", "company"),
        create_user("hr@zoho.com", "password", "company", False),
        create_user("hr@amazon.com", "password", "company"),
        create_user("hr@apple.com", "password", "company", False)
    ]

    db.session.add_all(student_users)
    db.session.add_all(company_users)

    db.session.commit()

    # ==================================================
    # STUDENTS
    # ==================================================

    students = [
        Student(
            user_id=student_users[0].user_id,
            name="Arjun Kumar",
            skills="Python, Flask, SQL",
            dept="CSE",
            course="BTech",
            cgpa=8.72,
            graduation_year=2027,
            backlog_count=0,
            resume="arjun_resume.pdf"
        ),
        Student(
            user_id=student_users[1].user_id,
            name="Priya Sharma",
            skills="Java, Spring Boot",
            dept="ISE",
            course="BTech",
            cgpa=9.12,
            graduation_year=2027,
            backlog_count=0,
            resume="priya_resume.pdf"
        ),
        Student(
            user_id=student_users[2].user_id,
            name="Rahul Verma",
            skills="React, NodeJS",
            dept="CSE",
            course="BTech",
            cgpa=8.45,
            graduation_year=2027,
            backlog_count=1,
            resume="rahul_resume.pdf"
        ),
        Student(
            user_id=student_users[3].user_id,
            name="Ananya Reddy",
            skills="VueJS, Flask",
            dept="AIML",
            course="BTech",
            cgpa=9.01,
            graduation_year=2027,
            backlog_count=0,
            resume="ananya_resume.pdf"
        ),
        Student(
            user_id=student_users[4].user_id,
            name="Vikram Singh",
            skills="JavaScript, MongoDB",
            dept="ECE",
            course="BTech",
            cgpa=7.95,
            graduation_year=2027,
            backlog_count=0,
            resume="vikram_resume.pdf"
        ),
        Student(
            user_id=student_users[5].user_id,
            name="Neha Patel",
            skills="Python, Data Analysis",
            dept="DS",
            course="BTech",
            cgpa=8.88,
            graduation_year=2027,
            backlog_count=0,
            resume="neha_resume.pdf"
        ),
        Student(
            user_id=student_users[6].user_id,
            name="Harshith M",
            skills="Python, Java",
            dept="DS",
            course="BTech",
            cgpa=8.0,
            graduation_year=2028,
            backlog_count=0,
            resume="harshith_resume.pdf"
        ),
    ]

    db.session.add_all(students)
    db.session.commit()

    # ==================================================
    # COMPANIES
    # ==================================================

    companies = [
        Company(
            user_id=company_users[0].user_id,
            name="TCS",
            industry="IT Services",
            location="Bangalore",
            website="https://www.tcs.com",
            status="approved"
        ),
        Company(
            user_id=company_users[1].user_id,
            name="Infosys",
            industry="IT Services",
            location="Mysore",
            website="https://www.infosys.com",
            status="approved"
        ),
        Company(
            user_id=company_users[2].user_id,
            name="Wipro",
            industry="IT Services",
            location="Bangalore",
            website="https://www.wipro.com",
            status="approved"
        ),
        Company(
            user_id=company_users[3].user_id,
            name="Accenture",
            industry="Consulting",
            location="Bangalore",
            website="https://www.accenture.com",
            status="approved"
        ),
        Company(
            user_id=company_users[4].user_id,
            name="Zoho",
            industry="Software",
            location="Chennai",
            website="https://www.zoho.com",
            status="removed"
        ),
        Company(
            user_id=company_users[5].user_id,
            name="Amazon",
            industry="E-Commerce",
            location="Hyderabad",
            website="https://www.amazon.jobs",
            status="approved"
        ),
        Company(
            user_id=company_users[6].user_id,
            name="Apple",
            industry="Tech",
            location="CA, USA",
            website="https://www.apple.jobs",
            status="pending"
        ),
    ]

    db.session.add_all(companies)
    db.session.commit()

    # ==================================================
    # DRIVES
    # ==================================================

    drives = [
        # Approved drives

        Drive(
            company_id=companies[0].company_id,
            job_title="Software Engineer",
            description="Backend development using Python",
            salary=700000,
            eligibility_cgpa=7.0,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="Python, SQL",
            deadline=date.today() + timedelta(days=20),
            status="approved"
        ),

        Drive(
            company_id=companies[1].company_id,
            job_title="System Engineer",
            description="Enterprise software solutions",
            salary=650000,
            eligibility_cgpa=7.0,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=1,
            required_skills="Java",
            deadline=date.today() + timedelta(days=15),
            status="approved"
        ),

        Drive(
            company_id=companies[2].company_id,
            job_title="Full Stack Developer",
            description="React and Flask development",
            salary=850000,
            eligibility_cgpa=7.5,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="React, Flask",
            deadline=date.today() + timedelta(days=30),
            status="approved"
        ),

        Drive(
            company_id=companies[3].company_id,
            job_title="Associate Consultant",
            description="Technology consulting",
            salary=900000,
            eligibility_cgpa=8.0,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="Communication",
            deadline=date.today() + timedelta(days=25),
            status="approved"
        ),

        Drive(
            company_id=companies[5].company_id,
            job_title="SDE-1",
            description="Amazon software engineer role",
            salary=1800000,
            eligibility_cgpa=8.5,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="DSA, Python",
            deadline=date.today() + timedelta(days=35),
            status="approved"
        ),

        Drive(
            company_id=companies[0].company_id,
            job_title="Data Analyst",
            description="Business intelligence role",
            salary=800000,
            eligibility_cgpa=7.0,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="SQL, Excel",
            deadline=date.today() + timedelta(days=22),
            status="approved"
        ),

        # closed drived

        Drive(
            company_id=companies[0].company_id,  # TCS
            job_title="Graduate Trainee",
            description="Recruitment completed",
            salary=600000,
            eligibility_cgpa=6.5,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=1,
            required_skills="Python, Aptitude",
            deadline=date.today() - timedelta(days=45),
            status="closed"
        ),

        Drive(
            company_id=companies[3].company_id,  # Accenture
            job_title="Technology Analyst",
            description="Applications closed",
            salary=950000,
            eligibility_cgpa=7.5,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="Problem Solving",
            deadline=date.today() - timedelta(days=20),
            status="closed"
        ),

        Drive(
            company_id=companies[5].company_id,  # Amazon
            job_title="Cloud Support Engineer",
            description="Drive completed",
            salary=1400000,
            eligibility_cgpa=8.0,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="AWS, Linux",
            deadline=date.today() - timedelta(days=10),
            status="closed"
        ),

        # Pending drives

        Drive(
            company_id=companies[5].company_id,
            job_title="ML Engineer",
            description="Awaiting admin approval",
            salary=1500000,
            eligibility_cgpa=8.0,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="Python, ML",
            deadline=date.today() + timedelta(days=40),
            status="pending"
        ),

        Drive(
            company_id=companies[1].company_id,
            job_title="Cloud Engineer",
            description="Awaiting admin approval",
            salary=1200000,
            eligibility_cgpa=7.5,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="AWS",
            deadline=date.today() + timedelta(days=45),
            status="pending"
        ),

        # Removed drives (Zoho)

        Drive(
            company_id=companies[4].company_id,
            job_title="Frontend Developer",
            description="Company removed",
            salary=1000000,
            eligibility_cgpa=8.0,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="VueJS",
            deadline=date.today() + timedelta(days=18),
            status="removed"
        ),

        Drive(
            company_id=companies[4].company_id,
            job_title="Backend Developer",
            description="Company removed",
            salary=1100000,
            eligibility_cgpa=8.0,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="Flask",
            deadline=date.today() + timedelta(days=20),
            status="removed"
        ),
    ]

    db.session.add_all(drives)
    db.session.commit()

    # ==================================================
    # APPLICATIONS
    # ==================================================

    applications = [

        Application(
            student_id=students[0].student_id,
            drive_id=drives[0].drive_id,
            current_status="selected"
        ),

        Application(
            student_id=students[1].student_id,
            drive_id=drives[1].drive_id,
            current_status="selected"
        ),

        Application(
            student_id=students[2].student_id,
            drive_id=drives[2].drive_id,
            current_status="rejected"
        ),

        Application(
            student_id=students[3].student_id,
            drive_id=drives[3].drive_id,
            current_status="shortlisted"
        ),

        Application(
            student_id=students[4].student_id,
            drive_id=drives[4].drive_id,
            current_status="applied"
        ),

        Application(
            student_id=students[5].student_id,
            drive_id=drives[5].drive_id,
            current_status="selected"
        ),

        # Company removed applications

        Application(
            student_id=students[0].student_id,
            drive_id=drives[8].drive_id,
            current_status="company_removed"
        ),

        Application(
            student_id=students[1].student_id,
            drive_id=drives[9].drive_id,
            current_status="company_removed"
        ),

        # Drive removed application example

        Application(
            student_id=students[2].student_id,
            drive_id=drives[8].drive_id,
            current_status="drive_removed"
        ),

        # closed drives (applications)
        Application(
            student_id=students[0].student_id,
            drive_id=drives[10].drive_id,
            current_status="selected"
        ),

        Application(
            student_id=students[2].student_id,
            drive_id=drives[11].drive_id,
            current_status="rejected"
        ),

        Application(
            student_id=students[5].student_id,
            drive_id=drives[12].drive_id,
            current_status="selected"
        ),

    ]

    db.session.add_all(applications)
    db.session.commit()

    # ==================================================
    # APPLICATION STATUS HISTORY
    # ==================================================

    statuses = []

    for application in applications:

        statuses.append(
            ApplicationStatus(
                application_id=application.application_id,
                status="applied"
            )
        )

        if application.current_status != "applied":
            statuses.append(
                ApplicationStatus(
                    application_id=application.application_id,
                    status=application.current_status
                )
            )

    db.session.add_all(statuses)

    # ==================================================
    # NOTIFICATIONS
    # ==================================================

    notifications = [
        Notification(
            student_id=students[0].student_id,
            title="Application Selected",
            message="You have been selected by TCS."
        ),
        Notification(
            student_id=students[1].student_id,
            title="Application Selected",
            message="You have been selected by Infosys."
        ),
        Notification(
            student_id=students[2].student_id,
            title="Application Rejected",
            message="Your Wipro application was rejected."
        ),
        Notification(
            student_id=students[3].student_id,
            title="Application Submitted",
            message="Application received successfully."
        ),
        Notification(
            student_id=students[4].student_id,
            title="Interview Scheduled",
            message="Interview scheduled for Zoho."
        ),
        Notification(
            student_id=students[5].student_id,
            title="Drive Reminder",
            message="Amazon drive closes soon."
        ),
    ]

    db.session.add_all(notifications)

    # ==================================================
    # PLACEMENTS
    # ==================================================

    placements = [
        Placement(
            student_id=students[0].student_id,
            company_id=companies[0].company_id,
            position="Software Engineer",
            salary=700000,
            joining_date=date(2027, 7, 1)
        ),
        Placement(
            student_id=students[1].student_id,
            company_id=companies[1].company_id,
            position="System Engineer",
            salary=650000,
            joining_date=date(2027, 7, 15)
        ),
        Placement(
            student_id=students[3].student_id,
            company_id=companies[3].company_id,
            position="Associate Consultant",
            salary=900000,
            joining_date=date(2027, 8, 1)
        ),
        Placement(
            student_id=students[5].student_id,
            company_id=companies[5].company_id,
            position="SDE-1",
            salary=1800000,
            joining_date=date(2027, 8, 15)
        ),
    ]

    db.session.add_all(placements)

    # ==================================================
    # INTERVIEWS
    # ==================================================

    interviews = [
        Interview(
            application_id=applications[0].application_id,
            type="online",
            feedback="Strong coding skills",
            scheduled_at=datetime.now() + timedelta(days=2),
            location="Google Meet"
        ),
        Interview(
            application_id=applications[1].application_id,
            type="online",
            feedback="Excellent communication",
            scheduled_at=datetime.now() + timedelta(days=3),
            location="Microsoft Teams"
        ),
        Interview(
            application_id=applications[2].application_id,
            type="offline",
            feedback="Needs improvement",
            scheduled_at=datetime.now() + timedelta(days=4),
            location="Wipro Bangalore"
        ),
        Interview(
            application_id=applications[3].application_id,
            type="online",
            feedback="Pending",
            scheduled_at=datetime.now() + timedelta(days=5),
            location="Zoom"
        ),
        Interview(
            application_id=applications[4].application_id,
            type="online",
            feedback="Selected",
            scheduled_at=datetime.now() + timedelta(days=6),
            location="Zoho Meet"
        ),
        Interview(
            application_id=applications[5].application_id,
            type="online",
            feedback="Pending",
            scheduled_at=datetime.now() + timedelta(days=7),
            location="Amazon Chime"
        ),
    ]

    db.session.add_all(interviews)

    db.session.commit()

    print("Database seeded successfully!")