from django import forms
from django.forms import ModelForm
from .models import *

from django.contrib.admin.widgets import *

class crearQueja(forms.ModelForm):
    viaje = forms.IntegerField(label = "ID Viaje", max_value = 6)
    cliente = forms.CharField(max_length = 60, required = True, label = 'Cliente Involucrado')
    descripcion = forms.CharField(max_length = 300, required = True, label = 'Descripción')
    class Meta:
        model = Queja
        fields = ['viaje', 'cliente', 'descripcion']

class crearSugerencia(forms.ModelForm):
    nombre = forms.CharField(max_length = 50, required = True, label = 'Nombre Sugerencia')
    motivacion = forms.CharField(max_length = 300, required = True, label = 'Motivo')
    descripcion = forms.CharField(max_length = 300, required = True, label ='Descripción')
    class Meta:
        model = Sugerencia
        fields = ['nombre', 'motivacion', 'descripcion']

class crearFalla(forms.ModelForm):
    secuencia = forms.CharField(max_length = 300, required = True, label = 'Secuencia de Pasos')
    contexto = forms.CharField(max_length = 300, required = True, label = 'Contexto Falla')
    class Meta:
        model = Queja
        fields = ['secuencia', 'contexto']