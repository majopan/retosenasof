# Generated by Django 5.1.1 on 2024-09-24 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resultados', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento'),
        ),
    ]
