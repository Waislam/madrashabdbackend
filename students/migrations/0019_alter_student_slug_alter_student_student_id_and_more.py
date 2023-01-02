# Generated by Django 4.1.2 on 2022-12-31 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_email'),
        ('students', '0018_alter_fessinfo_fees_type_term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='student',
            unique_together={('student_id', 'madrasha')},
        ),
    ]