# Generated by Django 4.1.2 on 2022-12-01 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('talimats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examroutine',
            name='exam_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='date_exams', to='talimats.examdate'),
        ),
    ]
