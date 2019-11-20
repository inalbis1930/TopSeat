from django import forms
from django.forms import ModelForm
from ..Modelo.models import *
import datetime
from django.contrib.admin.widgets import *
'''
    Archivo que contiene las clases para crear formularios con respecto a los CRUD's de los viajes y sus asociaciones.
'''

class form_crearViaje(forms.ModelForm):
    '''
        Formulario para crear un viaje con todos los campos necesarios y sus formatos,
        Solo puede crear viajes con vehiculos propios
    '''
    puestos_d = forms.IntegerField(label="Puestos Disponibles",max_value=6)
    fecha = forms.DateField(input_formats=['%d/%m/%Y'],widget =forms.DateInput(),help_text="DD/MM/AAAA")
    hora = forms.TimeField(input_formats=['%H:%M'],widget =forms.TimeInput(),help_text="HH:MM (En horario Militar)")
    #vehiculo = forms.ModelMultipleChoiceField(queryset=None,required= True, widget=forms.RadioSelect)
    tarifa =forms.IntegerField()
    class Meta:
        model = Viaje
        fields =['puestos_d','fecha','hora','vehiculo','tarifa']
    def __init__(self, user,*args, **kwargs):
        super(form_crearViaje,self).__init__(*args, **kwargs)
        self.fields['vehiculo'].queryset = Vehiculo.objects.filter(dueno=user) #Query para obtener solo los Vehiculos propios del usuario
        
class form_CrearRuta(forms.ModelForm):
    '''
        Formulario que va conjunto al de crear un Viaje, para crear una ruta asociada.
    '''
    inicio=forms.CharField(max_length=254,required= True,label='Direccion de Inicio')
    fin=forms.CharField(max_length=254,required= True,label='Direccion de Fin')
    class Meta:
        model = Ruta
        fields = ['inicio','fin']
        
class modificarViaje(forms.ModelForm):
    '''
        Formulario para modificar alguno o varios de los campos de un viaje, por esto ninguno es requerido,
        pero en caso de ser necesario tiene la opcion de modificar todos sus campos
    '''
    puestos_d = forms.IntegerField(label="Puestos Disponibles",max_value=6,required= False)
    fecha = forms.DateField(input_formats=['%d/%m/%Y'],widget =forms.DateInput(),required= False)
    hora = forms.TimeField(input_formats=['%H:%M'],widget =forms.TimeInput(),required= False)
    #vehiculo = forms.ModelMultipleChoiceField(queryset=Vehiculo.objects.filter())
    tarifa =forms.IntegerField(required= False)
    class Meta:
        model = Viaje
        fields =['puestos_d','fecha','hora','vehiculo','tarifa']
        
class modificarRuta(forms.ModelForm):
    '''
        Formulario para Modificar la ruta de un viaje asociado.
    '''
    inicio=forms.CharField(max_length=254,required= False,label='Direccion de Inicio')
    fin=forms.CharField(max_length=254,required= False,label='Direccion de Fin')
    class Meta:
        model = Ruta
        fields = ['inicio','fin']

class f_confirmarReserva(forms.ModelForm):
    '''
        Formulario que concreta la creacion de una reserva en un viaje. La cantidad de puestos dentro del viaje
        es necesaria, mas la parada no ya que el cliente puede no necesitar una parada.
    '''
    cantidadPuestos=forms.IntegerField(required= True,label='*Puestos Solicitados')
    parada=forms.CharField(max_length=254,required= False,label='Parada a Relizar')
    class Meta:
        model = Reserva
        fields = ['cantidadPuestos','parada']