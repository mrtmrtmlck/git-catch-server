from apscheduler.schedulers.background import BackgroundScheduler

from services import email_service


def schedule_issue_emails():
    scheduler = BackgroundScheduler()
    scheduler.add_job(email_service.send_issues, 'cron', hour=12, minute=40)
    scheduler.add_job(email_service.send_issues, 'cron', hour=15, minute=0)
    scheduler.add_job(email_service.send_issues, 'cron', hour=20, minute=0)
    scheduler.start()
