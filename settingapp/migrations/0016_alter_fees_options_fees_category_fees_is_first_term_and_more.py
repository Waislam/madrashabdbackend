# Generated by Django 4.1.2 on 2022-12-23 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_email'),
        ('settingapp', '0015_alter_fees_options_remove_fees_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fees',
            options={'ordering': ['term_name']},
        ),
        migrations.AddField(
            model_name='fees',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='settingapp.feescategory'),
        ),
        migrations.AddField(
            model_name='fees',
            name='is_first_term',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fees',
            name='is_second_term',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fees',
            name='is_third_term',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fees',
            name='term_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='feescategory',
            name='madrash',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='madrasha_fees_category', to='accounts.madrasha'),
        ),
        migrations.AlterField(
            model_name='fees',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='fees',
            unique_together={('term_name', 'madrasha')},
        ),
        migrations.RemoveField(
            model_name='fees',
            name='name',
        ),
    ]