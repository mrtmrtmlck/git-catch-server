import datetime
from decouple import config
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from issue_catcher import utils
from issue_catcher.models import User
from issue_catcher.templates import enums
from services import issue_service


def send_issues():
    all_issues = issue_service.get_issues()
    if len(all_issues) == 0:
        return

    subject = f'[GitCatch] There Are New Issues For You - {datetime.datetime.now():%Y-%m-%d %H:%M}'
    from_email = config('FROM_EMAIL')
    users = User.objects.all()
    for user in users:
        user_issues = issue_service.get_issues_by_user(all_issues, user.id)
        if len(user_issues) == 0:
            continue
        print("Issues title: " + user_issues[0]['title'])
        unsubscription_url = utils.get_url(enums.UrlExtension.UNSUBSCRIBE, {'email': user.email})
        params = {'issues': user_issues, 'unsubscription_url': unsubscription_url}
        html_message = render_to_string('email_templates/issues.html', params)
        plain_message = strip_tags(html_message)
        print("message created: " + plain_message)
        mail.send_mail(subject, plain_message, from_email, [user.email], html_message=html_message, fail_silently=False)

    print("SUCCESS!!!")


def send_verification_email(to_email, token_dict):
    subject = '[GitCatch] Please verify your email address'
    from_email = config('FROM_EMAIL')
    text_content = 'This is an important message.'
    subscription_url = utils.get_url(enums.UrlExtension.SUBSCRIBE, token_dict)
    html_content = f'<a href="{subscription_url}">Complete Subscription</a>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
