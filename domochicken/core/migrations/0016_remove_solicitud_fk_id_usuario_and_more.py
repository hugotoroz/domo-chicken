# Generated by Django 4.1.3 on 2023-05-24 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_solicitud_cantidad_solicitud'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud',
            name='fk_id_usuario',
        ),
        migrations.AddField(
            model_name='solicitud',
            name='realizado_por',
            field=models.CharField(max_length=50, null=True),
        ),
    ]