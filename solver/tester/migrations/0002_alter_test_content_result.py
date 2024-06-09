# Generated by Django 5.0.3 on 2024-04-26 11:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='content',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.JSONField(blank=True, default=None, null=True, verbose_name='Ответы')),
                ('numbers_of_correct', models.IntegerField(verbose_name='Число верных')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tester.test', verbose_name='Тест')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]