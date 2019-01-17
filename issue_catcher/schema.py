import graphene
from graphene_django import DjangoObjectType

from issue_catcher.models import Language, Label, User


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language


class LabelType(DjangoObjectType):
    class Meta:
        model = Label


class SubscribeUser(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        email = graphene.String()
        label_id_list = graphene.List(graphene.Int)
        language_id_list = graphene.List(graphene.Int)

    def mutate(self, info, label_id_list, language_id_list, email):
        user = User(email=email)
        user.save()
        labels = Label.objects.filter(id__in=label_id_list)
        user.labels.add(*labels)
        languages = Language.objects.filter(id__in=language_id_list)
        user.languages.add(*languages)

        return SubscribeUser(id=user.id)


class Query(object):
    languages = graphene.List(LanguageType)
    labels = graphene.List(LabelType)

    def resolve_languages(self, info):
        return Language.objects.all()

    def resolve_labels(self, info):
        return Label.objects.all()


class Mutation(graphene.ObjectType):
    subscribe_user = SubscribeUser.Field()
