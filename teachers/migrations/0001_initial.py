# Generated by Django 4.1.2 on 2023-01-02 08:50

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('settingapp', '0001_initial'),
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree_name', models.CharField(blank=True, max_length=255, null=True)),
                ('institution_name', models.CharField(blank=True, max_length=255, null=True)),
                ('passing_year', models.CharField(blank=True, max_length=255, null=True)),
                ('result', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_id', models.CharField(blank=True, max_length=20, unique=True)),
                ('father_name', models.CharField(blank=True, max_length=150, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=150, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=20, null=True)),
                ('religion', models.CharField(blank=True, choices=[('islam', 'Islam'), ('shonaton', 'Shonaton'), ('other', 'Other')], default='islam', max_length=20, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('married', 'Married'), ('unmarried', 'Unmarried')], default='married', max_length=15, null=True)),
                ('phone_home', models.CharField(blank=True, max_length=15, null=True)),
                ('nid', models.CharField(max_length=200)),
                ('birth_certificate', models.CharField(blank=True, max_length=255, null=True)),
                ('nationality', models.CharField(choices=[('bangladeshi', 'Bangladeshi'), ('indian', 'Indian'), ('other', 'Other')], default='bangladeshi', max_length=20)),
                ('blood_group', models.CharField(blank=True, max_length=15)),
                ('starting_date', models.DateField(default=datetime.date.today)),
                ('ending_date', models.DateField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_teachers', to='settingapp.department')),
                ('designation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designated_teachers', to='settingapp.designation')),
                ('education', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_educations', to='teachers.education')),
                ('experience', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_experience', to='teachers.experience')),
                ('madrasha', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='madrasha_teachers', to='accounts.madrasha')),
                ('permanent_address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='permanent_addres', to='accounts.address')),
                ('present_address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='present_addres', to='accounts.address')),
                ('skill', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_skills', to='teachers.skill')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='teachers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
