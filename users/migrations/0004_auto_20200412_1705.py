# Generated by Django 3.0.5 on 2020-04-12 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='', max_length=30),
        ),
    ]
