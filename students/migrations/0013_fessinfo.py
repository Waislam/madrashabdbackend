# Generated by Django 4.1.2 on 2022-12-09 17:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_alter_parent_occupation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FessInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_name', models.CharField(blank=True, max_length=255, null=True)),
                ('for_month', models.CharField(blank=True, max_length=100, null=True)),
                ('for_exam_term', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.CharField(blank=True, max_length=20, null=True)),
                ('paid_date', models.DateField(default=datetime.date.today)),
                ('is_paid', models.BooleanField(default=False)),
            ],
        ),
    ]
