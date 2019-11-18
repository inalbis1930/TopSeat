from django import forms
from django.forms import ModelForm
from ..Modelo.models import *
from Viajes.Modelo.models import *
from django.contrib.admin.widgets import *


'''
    Formulario para crear una queja nueva, debe tener asociado un viaje y un cliente acusado, con una descripcion
'''
class crearQuejaF(forms.ModelForm):
    viaje = forms.ModelChoiceField(queryset=Viaje.objects.all())
    clienteAcusado = forms.CharField(max_length = 60, required = True, label = 'Cliente Involucrado')
    descripcion = forms.CharField(max_length = 300, required = True, label = 'Descripción')
    class Meta:
        model = Queja
        fields = ['viaje', 'clienteAcusado', 'descripcion']
    '''def __init__(self, user,*args, **kwargs):
        super(crearQuejaF,self).__init__(*args, **kwargs)
        self.fields['viaje'].queryset = Viaje.objects.filter(conductor__usuario=user).union(Reserva.objects.filter(pasajero__usuario=user).only("viaje"))'''

'''
    Formulario para crear una sugerencia nueva, debe ser llenado por completo por el ciente.
'''
class crearSugerenciaF(forms.ModelForm):
    nombre = forms.CharField(max_length = 50, required = True, label = 'Nombre Sugerencia')
    motivacion = forms.CharField(max_length = 300, required = True, label = 'Motivo')
    descripcion = forms.CharField(max_length = 300, required = True, label ='Descripción')
    class Meta:
        model = Sugerencia
        fields = ['nombre', 'motivacion', 'descripcion']

'''
    Formulario para crear una sugerencia nueva, debe ser llenado por completo por el ciente.
'''
class crearFallaF(forms.ModelForm):
    secuencia = forms.CharField(max_length = 300, required = True, label = 'Secuencia de Pasos')
    contexto = forms.CharField(max_length = 300, required = True, label = 'Contexto Falla')
    class Meta:
        model = Falla
        fields = ['secuencia', 'contexto']

'''
    Formulario para responder un evento y dejarlo como terminado.
'''
class responderQueja(forms.ModelForm):
    respuesta = forms.CharField(max_length = 300, required = True, label = 'Respuesta')
    class Meta:
        model = Queja
        fields = ['respuesta']
'''
    Formulario para responder un evento y dejarlo como terminado.
'''
class responderSugerencia(forms.ModelForm):
    agradecimiento = forms.CharField(max_length = 300, required = True, label = 'Respuesta')
    class Meta:
        model = Sugerencia
        fields = ['agradecimiento']

'''
    Formulario para responder un evento y dejarlo como terminado.
'''
class responderFalla(forms.ModelForm):
    respuesta = forms.CharField(max_length = 300, required = True, label = 'Respuesta')
    class Meta:
        model = Falla
        fields = ['respuesta']
'''
    Formulario para elevar evento a un Evento mayor para ser atendido con mas urgencia
'''
class reportarEventoMayor(forms.ModelForm):
    justificacion=forms.CharField(max_length = 500, required = True, label = 'justificacion')
    class Meta:
        model = EventoMayor
        fields = ['justificacion']

