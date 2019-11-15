# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from django import forms
from .roles import *

# Create your models here.
"""

Clase Perfil
Representa a los usuarios en TopSeat. Permite a usuario ejercer de conductor o pasajero dentro del sistema.
Atributos:
"""
class Perfil(models.Model):
    id= models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User,on_delete=models.CASCADE)
    rol= models.IntegerField(choices=ROLES,default=1) 
    correo = models.EmailField()
    celular = models.CharField(max_length=12,default='0')
    def __str__(self):
        if self.rol == 1:
            rolAct="Pasajero"
        else:
            rolAct="Conductor"
        return str(self.usuario.username)+ " --> " + rolAct
        
class Vehiculo(models.Model):
    id = models.AutoField(primary_key=True)
    modelo = models.CharField(max_length=50)
    placa =models.CharField(max_length=6)
    color= models.CharField(max_length=20)
    dueno= models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.modelo) +" "+ self.placa