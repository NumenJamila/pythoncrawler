# Generated by Django 2.0.2 on 2018-08-25 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferenceinfo', '0002_auto_20180818_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='taskname',
            field=models.CharField(default='null', max_length=500),
        ),
    ]
