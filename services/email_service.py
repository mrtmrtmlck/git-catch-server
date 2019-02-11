from time import strftime, gmtime

from decouple import config
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from issue_catcher.models import User
from services import issue_service


def send_issues():
    current_time = strftime('%d/%m/%Y %H:%M:%S', gmtime())
    subject = f'[GitCatch] There Are New Issues For You - {current_time}'
    from_email = config('FROM_EMAIL')
    users = User.objects.all()
    for user in users:
        issues = issue_service.get_issues_by_user(user.id)
        if len(issues) == 0:
            continue
        print("Issues title: " + issues[0]['title'])
        html_message = render_to_string('email_templates/issues.html', {'issues': issues})
        plain_message = strip_tags(html_message)
        print("message created: " + plain_message)
        mail.send_mail(subject, plain_message, from_email, [user.email], html_message=html_message, fail_silently=False)

    print("SUCCESS!!!")


def send_verification_email(to_email, token):
    subject = '[GitCatch] Please verify your email address'
    from_email = config('TEST_FROM_EMAIL')
    text_content = 'This is an important message.'
    html_content = f'<a href="http://localhost:3000/completeSubscription?token={token}">Complete Subscription</a>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
