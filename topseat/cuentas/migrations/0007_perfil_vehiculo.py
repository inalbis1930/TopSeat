# Generated by Django 2.2.6 on 2019-10-16 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0007_auto_20191016_2110'),
        ('cuentas', '0006_remove_perfil_ruta'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='vehiculo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aplicacion.Vehiculo'),
        ),
    ]
