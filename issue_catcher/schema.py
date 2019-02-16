import graphene
from graphene_django import DjangoObjectType

from issue_catcher import utils
from issue_catcher.exceptions import DuplicateValueError
from issue_catcher.models import Language, Label, User
from services import email_service, user_service


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language


class LabelType(DjangoObjectType):
    class Meta:
        model = Label


class SendVerificationEmail(graphene.Mutation):
    success = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        email = graphene.String()
        label_id_list = graphene.List(graphene.Int)
        language_id_list = graphene.List(graphene.Int)

    def mutate(self, info, email, label_id_list, language_id_list):
        try:
            if not email or not label_id_list or not language_id_list:
                return SendVerificationEmail(success=False, error='All values should be given')

            elif User.objects.filter(email=email).exists():
                return SendVerificationEmail(success=False, error='Email already exists')

            token_dict = {'email': email, 'label_id_list': label_id_list, 'language_id_list': language_id_list}
            token = utils.generate_token(token_dict)
            email_service.send_verification_email(email, token)

            return SendVerificationEmail(success=True)
        except:
            return SendVerificationEmail(success=False, error='Unexpected error occurred')


class SubscribeUser(graphene.Mutation):
    success = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        token = graphene.String()

    def mutate(self, info, token):
        try:
            subscription_info = utils.decode_token(token)
            user_service.subscribe_user(subscription_info)

            return SubscribeUser(success=True)
        except ValueError:
            return SubscribeUser(success=False, error='All values must be given')
        except DuplicateValueError:
            return SubscribeUser(success=False, error='Data already exists')
        except Exception:
            return SubscribeUser(success=False, error='Unexpected error occurred')


class UnsubscribeUser(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        email = graphene.String()

    def mutate(self, info, email):
        try:
            User.objects.filter(email=email).delete()

            return UnsubscribeUser(success=True)
        except:
            return UnsubscribeUser(success=False)


class Query(object):
    languages = graphene.List(LanguageType)
    labels = graphene.List(LabelType)

    def resolve_languages(self, info):
        return Language.objects.all()

    def resolve_labels(self, info):
        return Label.objects.all()


class Mutation(graphene.ObjectType):
    send_verification_email = SendVerificationEmail.Field()
    subscribe_user = SubscribeUser.Field()
    unsubscribe_user = UnsubscribeUser.Field()
