# Generated by Django 4.0.5 on 2022-07-09 13:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_checker_essayevaluation_evaluator'),
    ]

    operations = [
        migrations.CreateModel(
            name='EssaySentenceReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence_number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Номер предложения должен быть положительным числом.')], verbose_name='Номер предложения сочинения')),
                ('evaluator_comment', models.CharField(max_length=1000, validators=[django.core.validators.MaxLengthValidator(1000, 'Комментарий не может быть длиннее 1000 символов.')], verbose_name='Комментарий проверяющего')),
                ('mistake_type', models.CharField(choices=[('K07', 'Орфографическая (К7)'), ('K08', 'Пунктуационная (К8)'), ('K09', 'Грамматическая (К9)'), ('K10', 'Речевая (К10)'), ('K11', 'Этическая (К11)'), ('K12', 'Фактическая (К12)')], max_length=3, verbose_name='Тип ошибки')),
                ('essay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.essay', verbose_name='Сочинение')),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Проверяющий')),
            ],
            options={
                'verbose_name': 'Предложение сочинения',
                'verbose_name_plural': 'Предложения сочинения',
            },
        ),
    ]
