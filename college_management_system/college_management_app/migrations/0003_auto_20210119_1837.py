# Generated by Django 3.1.2 on 2021-01-19 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college_management_app', '0002_auto_20210119_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavereportteacher',
            name='leave_status',
            field=models.IntegerField(default=0),
        ),
    ]
