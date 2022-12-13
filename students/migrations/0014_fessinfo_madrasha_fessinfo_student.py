# Generated by Django 4.1.2 on 2022-12-09 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_email'),
        ('students', '0013_fessinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='fessinfo',
            name='madrasha',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='madrasha_student_fees_info', to='accounts.madrasha'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fessinfo',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.student'),
        ),
    ]
