# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from django import forms
from ..roles import *

# Create your models here.
"""

Clase UsuarioTopSeat
Representa a los usuarios en TopSeat. Permite a usuario ejercer de conductor o pasajero dentro del sistema.
"""
class UsuarioTopSeat(models.Model):
    id= models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User,on_delete=models.CASCADE)
    rol= models.IntegerField(choices=ROLES,default=1) 
    correo = models.EmailField() #Solo puede ser @javeriana.edu.co
    celular = models.CharField(max_length=12,default='0') #Ideal que tenga WA
    fotoPerfil = models.ImageField(default = None,null=True,blank=True,upload_to = 'static/img/FotosPerfil')
    def __str__(self):
        if self.rol == 1:
            rolAct="Pasajero"
        else:
            rolAct="Conductor"
        return str(self.usuario.username)+ " --> " + rolAct
    
   

 
'''
    Vehiculo que puede ser utilizado en un viaje, esta relacionado con un solo dueño.
''' 
class Vehiculo(models.Model):
    id = models.AutoField(primary_key=True)
    modelo = models.CharField(max_length=50)
    placa =models.CharField(max_length=6)
    color= models.CharField(max_length=20)
    dueno= models.ForeignKey(User,on_delete=models.CASCADE) #Llave foranea del dueño del carro.
    
    def __str__(self):
        return str(self.modelo) +" "+ self.placa