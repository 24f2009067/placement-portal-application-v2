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
    # DATE HELPERS (for backdating records into last month)
    # ==================================================
    # Mirrors the exact window tasks.placementReport() queries against, so
    # anything stamped with prev_month_day(...) is guaranteed to be picked
    # up by that task, and anything left at its default (now) is
    # guaranteed NOT to be.

    now_dt = datetime.now()
    first_day_this_month = now_dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_prev_month = first_day_this_month - timedelta(days=1)
    start_of_prev_month = end_of_prev_month.replace(day=1)

    def prev_month_day(n, hour=10):
        """A datetime n days after the 1st of last month, at the given hour.
        Clamped so it can never fall on/after end_of_prev_month, even for
        short months like February."""
        days_in_prev_month = (end_of_prev_month - start_of_prev_month).days
        n = max(0, min(n, days_in_prev_month - 1))
        d = start_of_prev_month + timedelta(days=n)
        return d.replace(hour=hour, minute=0, second=0, microsecond=0)

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
        create_user("hr@amazon.com", "password", "company"),
        create_user("hr@zoho.com", "password", "company", False),
        create_user("hr@apple.com", "password", "company"),
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
            resume=""
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
            resume=""
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
            resume=""
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
            resume=""
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
            resume=""
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
            resume=""
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
            resume=""
        ),
    ]

    db.session.add_all(students)
    db.session.commit()

    # ==================================================
    # COMPANIES
    # ==================================================
    # NOTE: a company's own status ("approved" / "pending" / "removed") is
    # independent from any single drive's status. Only Zoho is "removed"
    # here, so it's the only company allowed to cascade "company_removed"
    # onto its applications below. Apple is "pending" (not yet approved by
    # admin) so it correctly has zero drives - a pending company hasn't
    # been cleared to post one yet.

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
            name="Amazon",
            industry="E-Commerce",
            location="Hyderabad",
            website="https://www.amazon.jobs",
            status="approved"
        ),
        Company(
            user_id=company_users[5].user_id,
            name="Zoho",
            industry="Software",
            location="Chennai",
            website="https://www.zoho.com",
            status="removed"
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
    # NOTE: every drive below belongs to a company that was actually
    # "approved" at the time the drive itself was posted/approved.
    # Amazon's second drive is "removed" even though Amazon (the company)
    # is still "approved" - that's an admin pulling one specific drive
    # without touching the company. Zoho's drive is "removed" because
    # Zoho itself was removed.

    drives = [
        Drive(
            company_id=companies[0].company_id,  # TCS
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
            company_id=companies[1].company_id,  # Infosys
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
            company_id=companies[2].company_id,  # Wipro
            job_title="Full Stack Developer",
            description="React and Flask development - hiring closed",
            salary=850000,
            eligibility_cgpa=7.5,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="React, Flask",
            deadline=date.today() - timedelta(days=5),
            status="closed"
        ),
        Drive(
            company_id=companies[3].company_id,  # Accenture
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
            company_id=companies[4].company_id,  # Amazon
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
            company_id=companies[4].company_id,  # Amazon - this drive removed by admin
            job_title="Cloud Support Engineer",
            description="Drive pulled by admin after posting",
            salary=1400000,
            eligibility_cgpa=8.0,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="AWS, Linux",
            deadline=date.today() + timedelta(days=10),
            status="removed"
        ),
        Drive(
            company_id=companies[5].company_id,  # Zoho - removed because company removed
            job_title="Frontend Developer",
            description="Company was removed from the platform",
            salary=1000000,
            eligibility_cgpa=8.0,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="VueJS",
            deadline=date.today() + timedelta(days=18),
            status="removed"
        ),
    ]

    db.session.add_all(drives)
    db.session.commit()

    # ==================================================
    # APPLICATIONS
    # ==================================================
    # NOTE: students can only ever apply while a drive is "approved"
    # (open) - never to one that's "pending" (not yet cleared by admin)
    # or already "removed". Neha and Harshith below applied while their
    # drive/company was still fine, and only afterwards did the drive
    # (Neha) or company (Harshith) get pulled - current_status reflects
    # that later cascade, not the original apply.

    applications = [

        Application(
            student_id=students[0].student_id,  # Arjun
            drive_id=drives[0].drive_id,         # TCS - approved
            current_status="selected"
        ),

        Application(
            student_id=students[1].student_id,  # Priya
            drive_id=drives[1].drive_id,         # Infosys - approved
            current_status="selected"
        ),

        Application(
            student_id=students[2].student_id,  # Rahul
            drive_id=drives[2].drive_id,         # Wipro - closed, already decided
            current_status="rejected"
        ),

        Application(
            student_id=students[3].student_id,  # Ananya
            drive_id=drives[3].drive_id,         # Accenture - approved
            current_status="shortlisted"
        ),

        Application(
            student_id=students[4].student_id,  # Vikram
            drive_id=drives[4].drive_id,         # Amazon SDE-1 - approved
            current_status="applied"
        ),

        Application(
            student_id=students[5].student_id,  # Neha
            drive_id=drives[5].drive_id,         # Amazon Cloud Support - now removed
            current_status="drive_removed"
        ),

        Application(
            student_id=students[6].student_id,  # Harshith
            drive_id=drives[6].drive_id,         # Zoho Frontend Dev - company removed
            current_status="company_removed"
        ),

    ]

    db.session.add_all(applications)
    db.session.commit()

    # ==================================================
    # APPLICATION STATUS HISTORY
    # ==================================================
    # Every application always starts "applied". Selected/rejected
    # candidates pass through "shortlisted" first; drive/company-removed
    # cascades attach directly to whatever stage the application was
    # already sitting at.

    statuses = [

        ApplicationStatus(application_id=applications[0].application_id, status="applied"),
        ApplicationStatus(application_id=applications[0].application_id, status="shortlisted"),
        ApplicationStatus(application_id=applications[0].application_id, status="selected"),

        ApplicationStatus(application_id=applications[1].application_id, status="applied"),
        ApplicationStatus(application_id=applications[1].application_id, status="shortlisted"),
        ApplicationStatus(application_id=applications[1].application_id, status="selected"),

        ApplicationStatus(application_id=applications[2].application_id, status="applied"),
        ApplicationStatus(application_id=applications[2].application_id, status="shortlisted"),
        ApplicationStatus(application_id=applications[2].application_id, status="rejected"),

        ApplicationStatus(application_id=applications[3].application_id, status="applied"),
        ApplicationStatus(application_id=applications[3].application_id, status="shortlisted"),

        ApplicationStatus(application_id=applications[4].application_id, status="applied"),

        ApplicationStatus(application_id=applications[5].application_id, status="applied"),
        ApplicationStatus(application_id=applications[5].application_id, status="drive_removed"),

        ApplicationStatus(application_id=applications[6].application_id, status="applied"),
        ApplicationStatus(application_id=applications[6].application_id, status="company_removed"),

    ]

    db.session.add_all(statuses)

    # ==================================================
    # NOTIFICATIONS
    # ==================================================
    # Each message matches what actually happened to that student's
    # application above - no notification announces an outcome the
    # student's data doesn't back up.

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
            title="Application Shortlisted",
            message="You have been shortlisted by Accenture."
        ),
        Notification(
            student_id=students[4].student_id,
            title="Application Submitted",
            message="Your application to Amazon (SDE-1) was received."
        ),
        Notification(
            student_id=students[5].student_id,
            title="Drive Removed",
            message="The Amazon Cloud Support Engineer drive was removed by the admin."
        ),
        Notification(
            student_id=students[6].student_id,
            title="Company Removed",
            message="Zoho was removed from the platform. Your application has been withdrawn."
        ),
    ]

    db.session.add_all(notifications)

    # ==================================================
    # PLACEMENTS
    # ==================================================
    # Only applications with current_status == "selected" get a
    # placement record - that's Arjun and Priya, and nobody else.

    placements = [
        Placement(
            student_id=students[0].student_id,
            company_id=companies[0].company_id,
            position="Software Engineer",
            salary=700000,
            joining_date=date.today() + timedelta(days=60)
        ),
        Placement(
            student_id=students[1].student_id,
            company_id=companies[1].company_id,
            position="System Engineer",
            salary=650000,
            joining_date=date.today() + timedelta(days=75)
        ),
    ]

    db.session.add_all(placements)

    # ==================================================
    # INTERVIEWS
    # ==================================================
    # Only applications that made it to at least "shortlisted" get an
    # interview record - applied-only (Vikram) and cascaded-away
    # (Neha, Harshith) applications never reached an interview.

    interviews = [
        Interview(
            application_id=applications[0].application_id,  # Arjun - selected
            type="online",
            feedback="Strong coding skills",
            scheduled_at=datetime.now() + timedelta(days=2),
            location="Google Meet"
        ),
        Interview(
            application_id=applications[1].application_id,  # Priya - selected
            type="online",
            feedback="Excellent communication",
            scheduled_at=datetime.now() + timedelta(days=3),
            location="Microsoft Teams"
        ),
        Interview(
            application_id=applications[2].application_id,  # Rahul - rejected after interview
            type="offline",
            feedback="Needs improvement on system design",
            scheduled_at=datetime.now() - timedelta(days=1),
            location="Wipro Bangalore"
        ),
        Interview(
            application_id=applications[3].application_id,  # Ananya - shortlisted
            type="online",
            feedback=None,
            scheduled_at=datetime.now() + timedelta(days=5),
            location="Zoom"
        ),
    ]

    db.session.add_all(interviews)

    db.session.commit()

    # ==================================================
    # PREVIOUS MONTH DATA (for monthly report demo)
    # ==================================================
    # tasks.placementReport() (Celery beat, runs 1st of every month) counts
    # anything created within the *previous* calendar month, by filtering
    # on each row's own created_on. Everything above was created "now" and
    # will NOT show up in that report - it'll only ever show 0s. This
    # section backdates a fresh company, student, drive, and application
    # data set into last month, using the same window math the task
    # itself uses, so there's something real for it to count.
    #
    # covers every counter the report computes:
    #   added_companies=2, blacklisted_companies=1 (Cognizant)
    #   added_students=2,  blacklisted_students=1  (Divya)
    #   added_drives=3,    closed_drives=1 (IBM Data Eng), blacklisted_drives=1 (Cognizant Trainee)
    #   added_applications=5, shortlisted=1, selected=1, rejected=1
    #     (+ 1 company_removed, + 1 plain "applied" - neither counted by
    #     name, but both correctly swell the added_applications total)

    prev_month_company_users = [
        create_user("hr@ibm.com", "password", "company"),               # approved
        create_user("hr@cognizant.com", "password", "company", False),  # blacklisted
    ]
    prev_month_company_users[0].created_on = prev_month_day(4)
    prev_month_company_users[1].created_on = prev_month_day(6)

    db.session.add_all(prev_month_company_users)
    db.session.commit()

    prev_month_companies = [
        Company(
            user_id=prev_month_company_users[0].user_id,
            name="IBM",
            industry="Technology",
            location="Bangalore",
            website="https://www.ibm.com",
            status="approved"
        ),
        Company(
            user_id=prev_month_company_users[1].user_id,
            name="Cognizant",
            industry="IT Services",
            location="Chennai",
            website="https://www.cognizant.com",
            status="removed"
        ),
    ]

    db.session.add_all(prev_month_companies)
    db.session.commit()

    prev_month_student_users = [
        create_user("karthik@student.com", "password", "student"),        # active
        create_user("divya@student.com", "password", "student", False),   # blacklisted
    ]
    prev_month_student_users[0].created_on = prev_month_day(2)
    prev_month_student_users[1].created_on = prev_month_day(20)

    db.session.add_all(prev_month_student_users)
    db.session.commit()

    prev_month_students = [
        Student(
            user_id=prev_month_student_users[0].user_id,
            name="Karthik R",
            skills="Java, AWS, Docker",
            dept="ISE",
            course="BTech",
            cgpa=8.3,
            graduation_year=2027,
            backlog_count=0,
            resume=""
        ),
        Student(
            user_id=prev_month_student_users[1].user_id,
            name="Divya S",
            skills="Python, SQL",
            dept="CSE",
            course="BTech",
            cgpa=7.6,
            graduation_year=2027,
            backlog_count=1,
            resume=""
        ),
    ]

    db.session.add_all(prev_month_students)
    db.session.commit()

    prev_month_drives = [
        Drive(
            company_id=prev_month_companies[0].company_id,  # IBM
            job_title="Cloud Engineer",
            description="Cloud infra role - still open",
            salary=1100000,
            eligibility_cgpa=7.5,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="AWS, Docker",
            deadline=date.today() + timedelta(days=20),
            status="approved"
        ),
        Drive(
            company_id=prev_month_companies[0].company_id,  # IBM
            job_title="Data Engineer",
            description="Hiring closed for this cycle",
            salary=1000000,
            eligibility_cgpa=7.5,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=0,
            required_skills="SQL, Spark",
            deadline=date.today() - timedelta(days=10),
            status="closed"
        ),
        Drive(
            company_id=prev_month_companies[1].company_id,  # Cognizant - company removed
            job_title="Trainee Engineer",
            description="Company was removed from the platform",
            salary=500000,
            eligibility_cgpa=6.5,
            eligibility_graduation_year=2027,
            eligibility_backlog_count=1,
            required_skills="Java",
            deadline=date.today() + timedelta(days=15),
            status="removed"
        ),
    ]
    prev_month_drives[0].created_on = prev_month_day(4)
    prev_month_drives[1].created_on = prev_month_day(6)
    prev_month_drives[2].created_on = prev_month_day(7)

    db.session.add_all(prev_month_drives)
    db.session.commit()

    prev_month_applications = [
        Application(
            student_id=prev_month_students[0].student_id,  # Karthik
            drive_id=prev_month_drives[0].drive_id,         # IBM Cloud Engineer
            current_status="selected"
        ),
        Application(
            student_id=prev_month_students[0].student_id,  # Karthik
            drive_id=prev_month_drives[1].drive_id,         # IBM Data Engineer
            current_status="shortlisted"
        ),
        Application(
            student_id=prev_month_students[1].student_id,  # Divya
            drive_id=drives[0].drive_id,                    # TCS Software Engineer (existing, approved)
            current_status="rejected"
        ),
        Application(
            student_id=prev_month_students[1].student_id,  # Divya
            drive_id=prev_month_drives[2].drive_id,         # Cognizant Trainee Engineer - company removed
            current_status="company_removed"
        ),
        Application(
            student_id=prev_month_students[1].student_id,  # Divya
            drive_id=prev_month_drives[0].drive_id,         # IBM Cloud Engineer
            current_status="applied"
        ),
    ]
    prev_month_applications[0].created_on = prev_month_day(10)
    prev_month_applications[1].created_on = prev_month_day(12)
    prev_month_applications[2].created_on = prev_month_day(14)
    prev_month_applications[3].created_on = prev_month_day(8)
    prev_month_applications[4].created_on = prev_month_day(15)

    db.session.add_all(prev_month_applications)
    db.session.commit()

    prev_month_statuses = [

        ApplicationStatus(application_id=prev_month_applications[0].application_id, status="applied", created_on=prev_month_day(10)),
        ApplicationStatus(application_id=prev_month_applications[0].application_id, status="shortlisted", created_on=prev_month_day(11)),
        ApplicationStatus(application_id=prev_month_applications[0].application_id, status="selected", created_on=prev_month_day(13)),

        ApplicationStatus(application_id=prev_month_applications[1].application_id, status="applied", created_on=prev_month_day(12)),
        ApplicationStatus(application_id=prev_month_applications[1].application_id, status="shortlisted", created_on=prev_month_day(14)),

        ApplicationStatus(application_id=prev_month_applications[2].application_id, status="applied", created_on=prev_month_day(14)),
        ApplicationStatus(application_id=prev_month_applications[2].application_id, status="shortlisted", created_on=prev_month_day(16)),
        ApplicationStatus(application_id=prev_month_applications[2].application_id, status="rejected", created_on=prev_month_day(18)),

        ApplicationStatus(application_id=prev_month_applications[3].application_id, status="applied", created_on=prev_month_day(8)),
        ApplicationStatus(application_id=prev_month_applications[3].application_id, status="company_removed", created_on=prev_month_day(9)),

        ApplicationStatus(application_id=prev_month_applications[4].application_id, status="applied", created_on=prev_month_day(15)),

    ]

    db.session.add_all(prev_month_statuses)

    prev_month_notifications = [
        Notification(
            student_id=prev_month_students[0].student_id,
            title="Application Selected",
            message="You have been selected by IBM.",
            created_on=prev_month_day(13)
        ),
        Notification(
            student_id=prev_month_students[0].student_id,
            title="Application Shortlisted",
            message="You have been shortlisted by IBM for Data Engineer.",
            created_on=prev_month_day(14)
        ),
        Notification(
            student_id=prev_month_students[1].student_id,
            title="Application Rejected",
            message="Your TCS application was rejected.",
            created_on=prev_month_day(18)
        ),
        Notification(
            student_id=prev_month_students[1].student_id,
            title="Company Removed",
            message="Cognizant was removed from the platform. Your application has been withdrawn.",
            created_on=prev_month_day(9)
        ),
    ]

    db.session.add_all(prev_month_notifications)

    prev_month_placements = [
        Placement(
            student_id=prev_month_students[0].student_id,
            company_id=prev_month_companies[0].company_id,  # IBM
            position="Cloud Engineer",
            salary=1100000,
            joining_date=date.today() + timedelta(days=45)
        ),
    ]

    db.session.add_all(prev_month_placements)

    prev_month_interviews = [
        Interview(
            application_id=prev_month_applications[0].application_id,  # Karthik - selected
            type="online",
            feedback="Great cloud fundamentals",
            scheduled_at=prev_month_day(11, hour=15),
            location="Google Meet"
        ),
        Interview(
            application_id=prev_month_applications[1].application_id,  # Karthik - shortlisted
            type="online",
            feedback=None,
            scheduled_at=prev_month_day(14, hour=11),
            location="Zoom"
        ),
        Interview(
            application_id=prev_month_applications[2].application_id,  # Divya - rejected after interview
            type="offline",
            feedback="Needs stronger fundamentals",
            scheduled_at=prev_month_day(16, hour=10),
            location="TCS Bangalore"
        ),
    ]

    db.session.add_all(prev_month_interviews)

    db.session.commit()

    print("Database seeded successfully! (includes last-month data for the monthly report demo)")