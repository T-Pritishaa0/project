# Generated by Django 3.1.2 on 2021-04-07 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college_management_app', '0008_studentfee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parents',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gender', models.CharField(max_length=255)),
                ('profile_pic', models.FileField(upload_to='')),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='college_management_app.courses')),
                ('session_year_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college_management_app.sessionyearmodel')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college_management_app.students')),
            ],
        ),
    ]
