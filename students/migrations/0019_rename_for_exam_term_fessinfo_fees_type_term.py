# Generated by Django 4.1.2 on 2022-12-15 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0018_fessinfo_student_income_alter_fessinfo_current_fee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fessinfo',
            old_name='for_exam_term',
            new_name='fees_type_term',
        ),
    ]