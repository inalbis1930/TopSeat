from django import forms
from django.forms import ModelForm
from .models import *
import datetime

from django.contrib.admin.widgets import *

class registrarVehiculo_f(forms.ModelForm):
    modelo = forms.CharField(max_length=50,required= True)
    placa = forms.CharField(max_length=6,required= True)
    color = forms.CharField(max_length=20,required= True)
    class Meta:
        model = Vehiculo
        fields =['modelo','placa','color']
        
        
class form_crearViaje(forms.ModelForm):
    puestos_d = forms.IntegerField(label="Puestos Disponibles",max_value=6)
    fecha = forms.DateField(input_formats=['%d/%m/%Y'],widget =forms.DateInput())
    hora = forms.TimeField(input_formats=['%H:%M'],widget =forms.TimeInput())
    #vehiculo = forms.ModelMultipleChoiceField(queryset=Vehiculo.objects.filter())
    tarifa =forms.IntegerField()
    class Meta:
        model = Viaje
        fields =['puestos_d','fecha','hora','vehiculo','tarifa']
        
class form_CrearRuta(forms.ModelForm):
    inicio=forms.CharField(max_length=254,required= True,label='Direccion de Inicio')
    fin=forms.CharField(max_length=254,required= True,label='Direccion de Fin')
    class Meta:
        model = Ruta
        fields = ['inicio','fin']