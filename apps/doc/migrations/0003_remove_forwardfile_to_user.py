# Generated by Django 3.2.6 on 2021-09-08 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0002_auto_20210908_0943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forwardfile',
            name='to_user',
        ),
    ]
