from django.db import transaction

from issue_catcher.models import User, Label, Language
from issue_catcher.exceptions import DuplicateValueError

def subscribe_user(user_info):
    try:
        if not user_info['email'] or not user_info['label_id_list'] or not user_info['language_id_list']:
            raise ValueError

        elif User.objects.filter(email=user_info['email']).exists():
            raise DuplicateValueError

        with transaction.atomic():
            user = User(email=user_info['email'])
            user.save()
            labels = Label.objects.filter(id__in=user_info['label_id_list'])
            user.labels.add(*labels)
            languages = Language.objects.filter(id__in=user_info['language_id_list'])
            user.languages.add(*languages)
    except:
        raise Exception

