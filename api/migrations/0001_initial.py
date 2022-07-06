# Generated by Django 4.0.5 on 2022-07-06 14:53

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vkontakte_id', models.PositiveIntegerField(blank=True, null=True)),
                ('telegram_id', models.PositiveIntegerField(blank=True, null=True)),
                ('rating', models.PositiveIntegerField(default=50, verbose_name='Рейтинг')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Essay',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('body', models.TextField(verbose_name='Поле для сочинения')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='works', to=settings.AUTH_USER_MODEL, verbose_name='Автор работы')),
            ],
            options={
                'verbose_name': 'Сочинение',
                'verbose_name_plural': 'Сочинения',
            },
        ),
        migrations.CreateModel(
            name='EssayCriteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('k1', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(1)], verbose_name='К1: Формулировка проблем исходного текста')),
                ('k2', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(6)], verbose_name='К2: Комментарий к сформулированной проблеме исходного текста')),
                ('k3', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(1)], verbose_name='К3: Отражение позиции автора исходного текста')),
                ('k4', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(1)], verbose_name='К4: Отношение к позиции автора по проблеме исходного текста')),
                ('k5', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(2)], verbose_name='К5: Смысловая цельность, речевая связность и последовательность изложения')),
                ('k6', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(2)], verbose_name='К6: Точность и выразительность речи')),
                ('k7', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(3)], verbose_name='К7: Соблюдение орфографических норм')),
                ('k8', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(3)], verbose_name='К8: Соблюдение пунктуационных норм')),
                ('k9', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(2)], verbose_name='К9: Соблюдение грамматических норм')),
                ('k10', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(2)], verbose_name='К10: Соблюдение речевых норм')),
                ('k11', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(1)], verbose_name='К11: Соблюдение этических норм')),
                ('k12', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(1)], verbose_name='К12: Соблюдение фактологической точности в фоновом материале')),
            ],
            options={
                'verbose_name': 'Критерий оценивая сочинения',
                'verbose_name_plural': 'Критерии оценивания сочинения',
            },
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(choices=[('S1', 'Нет задания'), ('S2', 'Приём работ'), ('S3', 'Приём проверок'), ('S4', 'Нет приёма работ')], default='S1', max_length=2, verbose_name='Этап')),
            ],
            options={
                'verbose_name': 'Этап',
                'verbose_name_plural': 'Этап',
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('body', models.TextField(verbose_name='Поле для текста')),
                ('author', models.CharField(max_length=75, verbose_name='Автор текста')),
                ('author_description', models.TextField(verbose_name='Описание автора текста')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='Учитель, который дал работу')),
            ],
            options={
                'verbose_name': 'Текст',
                'verbose_name_plural': 'Тексты',
            },
        ),
        migrations.CreateModel(
            name='WeekID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_year_from', models.PositiveIntegerField(default=2022, validators=[django.core.validators.MinValueValidator(1970), django.core.validators.MaxValueValidator(2999)], verbose_name='Начало учебного года')),
                ('study_year_to', models.PositiveIntegerField(default=2023, validators=[django.core.validators.MinValueValidator(1970), django.core.validators.MaxValueValidator(2999)], verbose_name='Конец учебного года')),
                ('week_number', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(250)], verbose_name='Номер учебной недели')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Номер недели',
                'verbose_name_plural': 'Номер недели',
            },
        ),
        migrations.CreateModel(
            name='TextKey',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('range_of_problems', models.TextField(verbose_name='Примерный круг проблем')),
                ('authors_position', models.TextField(verbose_name='Авторская позиция')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keys', to='api.text', verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Ключ к тексту',
                'verbose_name_plural': 'Ключи к тексту',
            },
        ),
        migrations.AddField(
            model_name='text',
            name='week_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task', to='api.weekid', verbose_name='Идентификатор недели'),
        ),
        migrations.CreateModel(
            name='FormURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(null=True, unique=True, verbose_name='Ссылка на форму')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_urls', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('week_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='form_urls', to='api.weekid', verbose_name='Номер недели')),
            ],
            options={
                'verbose_name': 'Ссылка на форму',
                'verbose_name_plural': 'Ссылки на формы',
            },
        ),
        migrations.CreateModel(
            name='EssayEvaluation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('checker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to=settings.AUTH_USER_MODEL, verbose_name='Проверяющий')),
                ('criteria', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation', to='api.essaycriteria', verbose_name='Критерии')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='api.essay', verbose_name='Работа')),
            ],
            options={
                'verbose_name': 'Проверка сочинений',
                'verbose_name_plural': 'Проверки сочинений',
            },
        ),
        migrations.AddField(
            model_name='essay',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='essays', to='api.text', verbose_name='Текст, по которому написано сочинение'),
        ),
    ]
