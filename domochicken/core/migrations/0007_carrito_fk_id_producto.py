# Generated by Django 4.1.3 on 2023-05-18 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_carrito_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrito',
            name='fk_id_producto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.producto'),
        ),
    ]