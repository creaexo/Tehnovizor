# Generated by Django 4.2.6 on 2023-10-24 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_dish_options_remove_dish_image4'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartdish',
            name='content_type',
        ),
        migrations.AlterField(
            model_name='dish',
            name='calories',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, verbose_name='Калории'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='carb',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, verbose_name='Углеводы'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='fats',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, verbose_name='Жиры'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='proteins',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, verbose_name='Белки'),
        ),
    ]
