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
    fecha = forms.DateField(input_formats=['%d/%m/%Y'],widget =forms.DateInput(),help_text="DD/MM/AAA")
    hora = forms.TimeField(input_formats=['%H:%M'],widget =forms.TimeInput(),help_text="HH:MM")
    #vehiculo = forms.ModelMultipleChoiceField(queryset=None,required= True, widget=forms.RadioSelect)
    tarifa =forms.IntegerField()
    class Meta:
        model = Viaje
        fields =['puestos_d','fecha','hora','vehiculo','tarifa']
    def __init__(self, user,*args, **kwargs):
        super(form_crearViaje,self).__init__(*args, **kwargs)
        self.fields['vehiculo'].queryset = Vehiculo.objects.filter(dueno=user)
        
class form_CrearRuta(forms.ModelForm):
    inicio=forms.CharField(max_length=254,required= True,label='Direccion de Inicio')
    fin=forms.CharField(max_length=254,required= True,label='Direccion de Fin')
    class Meta:
        model = Ruta
        fields = ['inicio','fin']
        
class modificarViaje(forms.ModelForm):
    puestos_d = forms.IntegerField(label="Puestos Disponibles",max_value=6,required= False)
    fecha = forms.DateField(input_formats=['%d/%m/%Y'],widget =forms.DateInput(),required= False)
    hora = forms.TimeField(input_formats=['%H:%M'],widget =forms.TimeInput(),required= False)
    #vehiculo = forms.ModelMultipleChoiceField(queryset=Vehiculo.objects.filter())
    tarifa =forms.IntegerField(required= False)
    class Meta:
        model = Viaje
        fields =['puestos_d','fecha','hora','vehiculo','tarifa']
        
class modificarRuta(forms.ModelForm):
    inicio=forms.CharField(max_length=254,required= False,label='Direccion de Inicio')
    fin=forms.CharField(max_length=254,required= False,label='Direccion de Fin')
    class Meta:
        model = Ruta
        fields = ['inicio','fin']

class f_confirmarReserva(forms.ModelForm):
    cantidadPuestos=forms.IntegerField(required= True,label='Puestos Solicitados')
    class Meta:
        model = Reserva
        fields = ['cantidadPuestos']