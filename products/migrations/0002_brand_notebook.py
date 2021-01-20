# Generated by Django 3.1.5 on 2021-01-19 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='Назва бренду')),
            ],
        ),
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_model', models.CharField(max_length=25, verbose_name='Модель')),
                ('img', models.ImageField(upload_to='', verbose_name='Зображення')),
                ('display', models.CharField(max_length=5, verbose_name='Діагональ')),
                ('rom', models.CharField(choices=[('HDD', 'HDD'), ('SSD', 'SSD'), ('HSD', 'HDD + SSD')], max_length=10, verbose_name="Тип пам'яті")),
                ('ram', models.CharField(choices=[('DDR2', 'DDR2'), ('DDR3', 'DDR3'), ('DDR4', 'DDR4')], max_length=10, verbose_name="Тип оперативної пам'яті")),
                ('fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.subcategory', verbose_name='Підкатегорія')),
                ('fk_brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.brand', verbose_name='Бренд')),
            ],
        ),
    ]
