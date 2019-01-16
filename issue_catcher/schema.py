import graphene
from graphene_django import DjangoObjectType

from issue_catcher.models import Language, Label


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language


class LabelType(DjangoObjectType):
    class Meta:
        model = Label


class Query(object):
    languages = graphene.List(LanguageType)
    labels = graphene.List(LabelType)

    def resolve_languages(self, info):
        return Language.objects.all()

    def resolve_labels(self, info):
        return Label.objects.all()
