# Generated by Django 3.2.6 on 2021-10-05 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0002_auto_20211005_0721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forwardfile',
            name='active',
        ),
        migrations.AddField(
            model_name='document',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
