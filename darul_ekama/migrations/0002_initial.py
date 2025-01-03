# Generated by Django 4.1.2 on 2023-01-02 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('settingapp', '0001_initial'),
        ('accounts', '0001_initial'),
        ('darul_ekama', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seatbooking',
            name='building',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='building_seats', to='settingapp.building'),
        ),
        migrations.AddField(
            model_name='seatbooking',
            name='madrasha',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='madrasha_seat_booking', to='accounts.madrasha'),
        ),
        migrations.AddField(
            model_name='seatbooking',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_seats', to='settingapp.room'),
        ),
        migrations.AddField(
            model_name='seatbooking',
            name='seat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booked_seat', to='settingapp.seat'),
        ),
    ]
