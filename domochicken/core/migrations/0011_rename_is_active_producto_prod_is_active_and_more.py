# Generated by Django 4.1.3 on 2023-05-23 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_carrito_fk_id_producto_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='is_active',
            new_name='prod_is_active',
        ),
        migrations.RenameField(
            model_name='proveedor',
            old_name='is_active',
            new_name='prov_is_active',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='is_active',
            new_name='u_is_active',
        ),
    ]