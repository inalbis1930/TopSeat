from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .roles import *
from . import models


class ProfileForm(forms.ModelForm):
    Nombre = forms.CharField(max_length=30,required=True)
    Apellido = forms.CharField(max_length=30,required=True)
    correo = forms.EmailField(max_length=254,required=True, help_text='Por favor introduzca su correo institucional de la P.U Javeriana')
    class Meta:
        model = models.Perfil
        fields = ('correo','rol')

class editarUsuario(forms.ModelForm):
    first_name = forms.CharField(label='Nombre',max_length=30,required=False)
    last_name = forms.CharField(label='Apellido',max_length=30,required=False)
    class Meta:
        model = User
        fields = ('first_name','last_name')