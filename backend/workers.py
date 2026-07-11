from celery import Celery
from celery.schedules import crontab

celery = Celery("Placement Postal 2")

def init_celery(app):

  celery.conf.update(
    broker_url = "redis://localhost:6379/0",
    result_backend = "redis://localhost:6379/1"
  )

  class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
      with app.app_context():
        return self.run(*args, **kwargs)
      
  celery.Task = ContextTask
  celery.conf.timezone = "Asia/Kolkata"
  celery.conf.enable_utc = False

  celery.conf.beat_schedule = {
    "interview_reminders" : {
      "task": "tasks.interviewReminders",
      "schedule": crontab(hour=7, minute=0),
      # "schedule": 10.0,
    },

    "placement-report": {
      "task": "tasks.placementReport",
      "schedule": crontab(day_of_month=1, hour=0, minute=0),
      # "schedule": 10.0
    },

    "auto-close-drives": {
      "task": "tasks.closeDrives",
      "schedule": crontab(hour=0, minute=0),
      # "schedule": 10.0
    }
  }

  import tasks

