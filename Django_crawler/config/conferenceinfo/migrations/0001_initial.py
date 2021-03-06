# Generated by Django 2.0.2 on 2018-07-19 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.CharField(default='null', max_length=500)),
                ('cnName', models.CharField(default='null', max_length=500)),
                ('enName', models.CharField(default='null', max_length=500)),
                ('introduce', models.CharField(default='null', max_length=3000)),
                ('location', models.CharField(default='null', max_length=500)),
                ('sponsor', models.CharField(default='null', max_length=500)),
                ('startdate', models.DateField(null=True)),
                ('enddate', models.DateField(null=True)),
                ('deadline', models.DateField(null=True)),
                ('image', models.CharField(default='null', max_length=500)),
                ('tag', models.CharField(default='null', max_length=500)),
            ],
        ),
    ]
