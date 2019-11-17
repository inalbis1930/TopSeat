from django.contrib import admin
from .Modelo.models import *

# Register your models here.

admin.site.register(Queja)
admin.site.register(Sugerencia)
admin.site.register(Falla)