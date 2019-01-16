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
    email = models.EmailField()
    language = models.ManyToManyField(Language)
    label = models.ManyToManyField(Label)

    def display_language(self):
        return ', '.join(lang.name for lang in self.language.all())

    def display_label(self):
        return ', '.join(label.name for label in self.label.all())

    display_language.short_description = 'Language'
    display_label.short_description = 'Label'

    def __str__(self):
        return self.email
