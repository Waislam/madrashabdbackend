# Generated by Django 4.1.2 on 2023-01-02 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
        ('settingapp', '0001_initial'),
        ('accounts', '0001_initial'),
        ('teachers', '0001_initial'),
        ('darul_ekama', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seatbooking',
            name='students',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_seat_dist', to='students.student'),
        ),
        migrations.AddField(
            model_name='nigranitable',
            name='building',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='building_nigrans', to='settingapp.building'),
        ),
        migrations.AddField(
            model_name='nigranitable',
            name='class_nigran',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_nigrans', to='settingapp.madrashaclasses'),
        ),
        migrations.AddField(
            model_name='nigranitable',
            name='madrasha',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='madrasha_darul_ekam_nigrani', to='accounts.madrasha'),
        ),
        migrations.AddField(
            model_name='nigranitable',
            name='room',
            field=models.ManyToManyField(blank=True, related_name='room_nigran', to='settingapp.room'),
        ),
        migrations.AddField(
            model_name='nigranitable',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher_nigrani', to='teachers.teacher'),
        ),
    ]
