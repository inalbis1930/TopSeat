# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from aplicacion.models import *
from django import forms
from .roles import *

# Create your models here.
"""

Clase Perfil
Representa a los usuarios en TopSeat. Permite a usuario ejercer de conductor o pasajero dentro del sistema.
Atributos:
"""
class Perfil(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.CASCADE)
    rol= models.IntegerField(choices=ROLES,default=1) 
    correo = models.EmailField()
    def __str__(self):
        if self.rol == 1:
            rolAct="Pasajero"
        else:
            rolAct="Conductor"
        return str(self.usuario.username)+ " --> " + rolAct
