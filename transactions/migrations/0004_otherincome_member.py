# Generated by Django 4.1.2 on 2022-12-27 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('committees', '0004_permanentmembers_monthly_activation_date_and_more'),
        ('transactions', '0003_rename_updated_cat_studentincome_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherincome',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='member_id', to='committees.permanentmembers'),
        ),
    ]
