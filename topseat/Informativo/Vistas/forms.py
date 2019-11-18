from django import forms
from django.forms import ModelForm
from ..Modelo.models import *
from django.contrib.admin.widgets import *

'''
    Formulario para poder reportar un bug a los desarralladores de la aplicacion.
'''
class reportarBug(forms.ModelForm):
    justificacion = forms.CharField(max_length = 700, required = True, label = 'Respuesta')
    class Meta:
        model = Bug
        fields = ['justificacion']
