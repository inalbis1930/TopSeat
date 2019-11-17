from django import forms
from django.forms import ModelForm
from ..Modelo.models import *
from Viajes.Modelo.models import *
from django.contrib.admin.widgets import *

class crearQueja(forms.ModelForm):
    viaje = forms.ModelChoiceField(queryset=Viaje.objects.all())#Falta
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
        model = Falla
        fields = ['secuencia', 'contexto']
##De aqui pa bajo falta###
class responderQueja(forms.ModelForm):
    respuesta = forms.CharField(max_length = 300, required = True, label = 'Respuesta')
    class Meta:
        model = Queja
        fields = ['respuesta']

class responderSugerencia(forms.ModelForm):
    agradecimiento = forms.CharField(max_length = 300, required = True, label = 'Respuesta')
    class Meta:
        model = Sugerencia
        fields = ['agradecimiento']


class responderFalla(forms.ModelForm):
    respuesta = forms.CharField(max_length = 300, required = True, label = 'Respuesta')
    class Meta:
        model = Falla
        fields = ['respuesta']