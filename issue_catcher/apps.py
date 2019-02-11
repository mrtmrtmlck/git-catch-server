from django.apps import AppConfig


class IssueCatcherConfig(AppConfig):
    name = 'issue_catcher'

    def ready(self):
        from services import schedule_service
        schedule_service.schedule_issue_emails()
