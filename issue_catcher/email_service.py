from decouple import config
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from issue_catcher.issue_service import get_issues_by_user
from issue_catcher.models import User


def send_email():
    subject = '[GitCatch] There Are New Issues For You'
    from_email = config('TEST_FROM_EMAIL')
    users = User.objects.all()
    for user in users:
        issues = get_issues_by_user(user.id)
        print("Issues title: " + issues[0]['title'])
        html_message = render_to_string('email_templates/issues.html', {'issues': issues})
        plain_message = strip_tags(html_message)
        print("message created: " + plain_message)
        mail.send_mail(subject, plain_message, from_email, [user.email], html_message=html_message)

    print("SUCCESS!!!")


def send_verification_email(to_email, token):
    subject = '[GitCatch] Please verify your email address'
    from_email = config('TEST_FROM_EMAIL')
    text_content = 'This is an important message.'
    html_content = f'<a href="http://localhost:3000/verify?token={token}">Verify your email.</a>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
