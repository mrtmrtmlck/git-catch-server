# Generated by Django 2.1.7 on 2019-02-16 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue_catcher', '0005_auto_20190216_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubrequestlog',
            name='request_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
