# Generated by Django 4.1.2 on 2022-12-10 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talimats', '0002_alter_examroutine_exam_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookdistributetoteacher',
            name='end_time',
            field=models.TimeField(default=None, null=True),
        ),
    ]
