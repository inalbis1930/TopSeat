# Generated by Django 2.2.7 on 2019-11-18 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Viajes', '0002_reserva_parada'),
    ]

    operations = [
        migrations.AddField(
            model_name='viaje',
            name='terminado',
            field=models.BooleanField(default=False),
        ),
    ]
