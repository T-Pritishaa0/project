# Generated by Django 3.1.2 on 2021-03-01 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('college_management_app', '0006_studentresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationteachers',
            name='teachers_id',
        ),
        migrations.DeleteModel(
            name='NotificationStudent',
        ),
        migrations.DeleteModel(
            name='NotificationTeachers',
        ),
    ]