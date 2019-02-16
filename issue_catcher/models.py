from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class User(models.Model):
    email = models.EmailField(unique=True)
    languages = models.ManyToManyField(Language)
    labels = models.ManyToManyField(Label)

    def display_language(self):
        return ', '.join(language.name for language in self.languages.all())

    def display_label(self):
        return ', '.join(label.name for label in self.labels.all())

    display_language.short_description = 'Language'
    display_label.short_description = 'Label'

    def __str__(self):
        return self.email


class GithubRequestLog(models.Model):
    label = models.CharField(max_length=50, unique=True)
    request_date = models.DateTimeField(auto_now_add=True)
