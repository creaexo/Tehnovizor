# Generated by Django 4.2.6 on 2023-10-23 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dish',
            options={'verbose_name': 'Блюдо', 'verbose_name_plural': ' Блюда'},
        ),
        migrations.RemoveField(
            model_name='dish',
            name='image4',
        ),
    ]
