# Generated by Django 4.0.5 on 2022-08-11 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_rename_evaluation_rateessayevaluation_evaluation_criteria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rateessayevaluation',
            name='evaluation_criteria',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='rate',
                to='api.essaycriteria',
                verbose_name='Проверка',
            ),
        ),
    ]
