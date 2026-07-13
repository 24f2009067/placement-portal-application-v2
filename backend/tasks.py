from workers import celery
import csv
import models
import os
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
from flask import render_template
import calendar

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

# utitlity
def sendEmail(subject, to, content, attachment_path=None, attachment_name=None, subtype="csv"):
  msg = EmailMessage()
  msg['subject'] = subject
  msg["From"] = MAIL_USERNAME
  msg["To"] = to

  msg.set_content(content)

  if attachment_path:
    with open(attachment_path, "rb") as f:
      msg.add_attachment(
        f.read(),
        maintype="text",
        subtype=subtype,
        filename=attachment_name
      )
  with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
    smtp.starttls()
    smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
    smtp.send_message(msg)

# CSV exports
@celery.task()
def generateStudentReport(student_id):
  student = models.Student.query.filter(models.Student.student_id == student_id).first()
  if student:
    os.makedirs("exports", exist_ok=True)

    file_name = f"{student.name}_{datetime.now()}.csv"
    with open(f"exports/{file_name}", "w", newline="", encoding="utf-8") as f:
      writer = csv.writer(f)
      writer.writerow([
          "Application ID",
          "Student ID",
          "Company",
          "Drive",
          "Status",
          "Applied On"
      ])

      for application in student.applications:
        writer.writerow([
          application.application_id,
          student.student_id,
          application.drive.company.name,
          application.drive.job_title,
          application.current_status,
          datetime.isoformat(application.created_on)
        ])

    if student.user.email.endswith("@gmail.com") or student.user.email.endswith("@ds.study.iitm.ac.in"):
      sendEmail("Placement Portal - Your Application History is Ready",
                student.user.email,
                """
Hello,

Your requested application history has been generated successfully.

The CSV report is attached to this email.

Regards,
Placement Portal Team
                """,
                f"exports/{file_name}",
                file_name
              )
      
      print("mail sent!")
    os.remove(f"exports/{file_name}")

    
    return file_name
  else:
    return "Error fetching student!"
  

@celery.task()
def generateCompanyReport(company_id):
  company = models.Company.query.filter(models.Company.company_id == company_id).first()
  if company:
    os.makedirs("exports", exist_ok=True)

    file_name = f"{company.name}_{datetime.now()}.csv"
    with open(f"exports/{file_name}", "w", newline="", encoding="utf-8") as f:
      writer = csv.writer(f)
      writer.writerow([
          "Application ID",
          "Student ID",
          "student name",
          "Drive",
          "Status",
          "Applied On"
      ])

      for drive in company.drives:
        for application in drive.applications:
          writer.writerow([
            application.application_id,
            application.student.student_id,
            application.student.name,
            application.drive.job_title,
            application.current_status,
            datetime.isoformat(application.created_on)
          ])

    if company.user.email.endswith("@gmail.com") or company.user.email.endswith("@ds.study.iitm.ac.in"):
      sendEmail("Placement Portal - Your Application History is Ready",
                company.user.email,
                """
Hello,

Your requested application history has been generated successfully.

The CSV report is attached to this email.

Regards,
Placement Portal Team
                """,
                f"exports/{file_name}",
                file_name
              )
      
      print("mail sent!")
    os.remove(f"exports/{file_name}")

    
    return file_name
  else:
    return "Error fetching student!"


# scheduled jobs

@celery.task()
def interviewReminders():
  today = datetime.now().date()
  
  start = datetime.combine(today, datetime.min.time())
  end = start + timedelta(days=2)

  interviews = models.Interview.query.filter(
    models.Interview.scheduled_at >= start,
    models.Interview.scheduled_at < end,
  ).all()

  for interview in interviews:
    email = interview.application.student.user.email

    if email.endswith("@gmail.com") or email.endswith("@ds.study.iitm.ac.in"):
      sendEmail("Placement Portal - Interview reminder",
                email,
                f"""
Hello {interview.application.student.name},

You have an interview scheduled on {interview.scheduled_at.strftime("%c")}.

Company: {interview.application.drive.company.name}
Drive: {interview.application.drive.job_title}
Mode: {interview.type}
Location: {interview.location}


All the best!

Regards,
Placement Portal Team
                """,
              )
      
      print("mail sent!")


@celery.task()
def placementReport():
  today = datetime.now()
  first_day_current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
  end_of_prev_month = first_day_current_month - timedelta(days=1)
  start_of_prev_month = end_of_prev_month.replace(day=1)
  
  students = models.Student.query.join(models.User).filter(
    models.User.created_on >= start_of_prev_month,
    models.User.created_on <= end_of_prev_month,
  )

  added_students = students.count()
  blacklisted_students = students.filter(models.User.is_active == False).count()

  companies = models.Company.query.join(models.User).filter(
    models.User.created_on >= start_of_prev_month,
    models.User.created_on <= end_of_prev_month,
  )

  added_companies = companies.count()
  blacklisted_companies = companies.filter(models.Company.status == "removed").count()

  drives = models.Drive.query.filter(
    models.Drive.created_on >= start_of_prev_month,
    models.Drive.created_on <= end_of_prev_month,
  )

  added_drives = drives.count()
  closed_drives = drives.filter(models.Drive.status == "closed").count()
  blacklisted_drives = drives.filter(models.Drive.status == "removed").count()

  applications = models.Application.query.filter(
    models.Application.created_on >= start_of_prev_month,
    models.Application.created_on <= end_of_prev_month,
  )

  added_applications = applications.count()
  shortlisted_applications = applications.filter(models.Application.current_status == "shortlisted").count()
  selected_applications = applications.filter(models.Application.current_status == "selected").count()
  rejected_applications = applications.filter(models.Application.current_status == "rejected").count()

  rendered_html = render_template(
    "adminReport.html", 
    today=today.date(),
    month = calendar.month_name[start_of_prev_month.month],
    added_students=added_students,
    blacklisted_students=blacklisted_students,

    added_companies = added_companies,
    blacklisted_companies = blacklisted_companies,

    added_drives = added_drives,
    closed_drives = closed_drives,
    blacklisted_drives = blacklisted_drives,

    added_applications = added_applications,
    shortlisted_applications = shortlisted_applications,
    selected_applications = selected_applications,
    rejected_applications = rejected_applications,
  )

  print(rendered_html)
  file_name = f'admin_report_{today.date()}.html'
  with open(f'exports/{file_name}', 'w', encoding='utf-8') as f:
    f.write(rendered_html)

  sendEmail("Placement Portal - Your Monthly Report is Ready",
            MAIL_USERNAME,
            """
Hello,

Your monthly placement report has been generated successfully.

The html report is attached to this email.

Regards,
Placement Portal Team
            """,

            f"exports/{file_name}",
            file_name,
            "html"
          )
  
  print("mail sent!")
  os.remove(f"exports/{file_name}")


# auto-close completed drives
@celery.task()
def closeDrives():
  
  today = datetime.now().date()

  drives = models.Drive.query.filter(models.Drive.deadline < today).all()
  print(drives)
  for drive in drives:
    if drive.status == "approved":
      drive.status = "closed"
  
  models.db.session.commit()
  return len(drives)
