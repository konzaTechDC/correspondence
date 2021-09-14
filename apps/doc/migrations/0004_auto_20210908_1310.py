# Generated by Django 3.2.6 on 2021-09-08 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
        ('doc', '0003_remove_forwardfile_to_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forwardfile',
            name='receiver',
        ),
        migrations.AddField(
            model_name='forwardfile',
            name='receivers',
            field=models.ManyToManyField(related_name='forwards', to='manager.Manager'),
        ),
    ]
