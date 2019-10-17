from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .roles import *
from . import models


class signUpForm(UserCreationForm):
    Nombre = forms.CharField(max_length=30,required=True)
    Apellido = forms.CharField(max_length=30,required=True)
    correo = forms.EmailField(max_length=254,required=True, help_text='Por favor introduzca su correo institucional de la P.U Javeriana')
    class Meta:
        model = User
        fields = ('username','Nombre','Apellido','correo','password1','password2')

class ProfileForm(forms.ModelForm):
    correo = forms.EmailField(max_length=254,required=True, help_text='Por favor introduzca su correo institucional de la P.U Javeriana')
    class Meta:
        model = models.Perfil
        fields = ('correo','rol')