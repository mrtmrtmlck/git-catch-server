# Generated by Django 2.1.7 on 2019-02-16 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue_catcher', '0003_auto_20190117_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='GithubRequestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField()),
            ],
        ),
    ]
