import base64
import json

import graphene
from django.db import transaction
from graphene_django import DjangoObjectType

from issue_catcher.email_service import send_verification_email
from issue_catcher.models import Language, Label, User


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language


class LabelType(DjangoObjectType):
    class Meta:
        model = Label


class VerifyUser(graphene.Mutation):
    succeed = graphene.Boolean()

    class Arguments:
        email = graphene.String()
        label_id_list = graphene.List(graphene.Int)
        language_id_list = graphene.List(graphene.Int)

    def mutate(self, info, email, label_id_list, language_id_list):
        token_dict = {'email': email, 'label_id_list': label_id_list, 'language_id_list': language_id_list}
        token = base64.urlsafe_b64encode(json.dumps(token_dict).encode('utf-8')).decode("utf-8")
        send_verification_email(email, token)

        return VerifyUser(succeed=True)


class SubscribeUser(graphene.Mutation):
    succeed = graphene.Boolean()

    class Arguments:
        token = graphene.String()

    def mutate(self, info, token):
        try:
            subscription_info = json.loads(base64.urlsafe_b64decode(token).decode('utf-8'))
            if not subscription_info['email'] or not subscription_info['label_id_list'] or not subscription_info['language_id_list']:
                raise ValueError()

            with transaction.atomic():
                user = User(email=subscription_info['email'])
                user.save()
                labels = Label.objects.filter(id__in=subscription_info['label_id_list'])
                user.labels.add(*labels)
                languages = Language.objects.filter(id__in=subscription_info['language_id_list'])
                user.languages.add(*languages)

                return SubscribeUser(succeed=True)
        except:
            raise Exception("Subscription unsuccessful")


class UnsubscribeUser(graphene.Mutation):
    succeed = graphene.Boolean()

    class Arguments:
        email = graphene.String()

    def mutate(self, info, email):
        User.objects.filter(email=email).delete()

        return UnsubscribeUser(succeed=True)


class Query(object):
    languages = graphene.List(LanguageType)
    labels = graphene.List(LabelType)

    def resolve_languages(self, info):
        return Language.objects.all()

    def resolve_labels(self, info):
        return Label.objects.all()


class Mutation(graphene.ObjectType):
    verify_user = VerifyUser.Field()
    subscribe_user = SubscribeUser.Field()
    unsubscribe_user = UnsubscribeUser.Field()
