# Generated by Django 4.1.3 on 2023-05-10 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_rename_apellido_usuario_apellido_usuario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrito',
            name='fk_id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
