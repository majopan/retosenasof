# Generated by Django 5.1.1 on 2024-09-25 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resultados', '0007_alter_resultadoprueba_grupo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resultadoprueba',
            old_name='grupo',
            new_name='grupo_sanguineo',
        ),
    ]
