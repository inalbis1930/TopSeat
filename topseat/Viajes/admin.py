from django.contrib import admin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from .Modelo.models import *


admin.site.register(Ruta)
admin.site.register(Vehiculo)
admin.site.register(Viaje)
admin.site.register(Reserva)