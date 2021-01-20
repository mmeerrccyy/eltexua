# Generated by Django 3.1.5 on 2021-01-19 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210119_1902'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notebook',
            old_name='_model',
            new_name='model',
        ),
        migrations.AlterField(
            model_name='notebook',
            name='ram_capacity',
            field=models.PositiveSmallIntegerField(verbose_name="Об'єм оперативної пам'яті, Гб"),
        ),
        migrations.AlterField(
            model_name='notebook',
            name='rom_capacity',
            field=models.PositiveSmallIntegerField(verbose_name="Об'єм пам'яті, Гб"),
        ),
    ]