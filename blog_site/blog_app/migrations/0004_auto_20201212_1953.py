# Generated by Django 3.1.4 on 2020-12-12 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0003_auto_20201212_1506'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'ordering': ['title'], 'verbose_name': 'Категория(ю)', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AddField(
            model_name='posts',
            name='on_main',
            field=models.BooleanField(default=False, verbose_name='Закрепленно'),
        ),
    ]