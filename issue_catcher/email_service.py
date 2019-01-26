from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from issue_catcher.issue_service import get_issues_by_user
from issue_catcher.models import User


def send_email():
    subject = '[GitCatch] There Are New Issues For You'
    from_email = 'pydev.mert@gmail.com'
    users = User.objects.all()
    for user in users:
        issues = get_issues_by_user(user.id)
        print("Issues title: " + issues[0]['title'])
        html_message = render_to_string('email_templates/issues.html', {'issues': issues})
        plain_message = strip_tags(html_message)
        print("message created: " + plain_message)
        mail.send_mail(subject, plain_message, from_email, [user.email], html_message=html_message)

    print("SUCCESS!!!")
