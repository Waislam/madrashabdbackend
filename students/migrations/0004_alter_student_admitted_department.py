# Generated by Django 4.1.2 on 2023-01-09 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settingapp', '0002_initial'),
        ('students', '0003_student_previous_exam_institute_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='admitted_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_students', to='settingapp.department'),
        ),
    ]
