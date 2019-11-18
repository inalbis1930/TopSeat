# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_google_maps import fields as map_fields
from AdmonCuentas.Modelo.models import *
from django.contrib.auth.models import User

# Create your models here.

#------------------------Cliente--------------------
class Ruta(models.Model):
    id = models.AutoField(primary_key=True)
    inicio = models.CharField(max_length=254)
    fin = models.CharField(max_length=254)
    def __str__(self):
        return self.inicio +" --> "+ self.fin

class Viaje(models.Model):
    id = models.AutoField(primary_key=True)
    conductor= models.ForeignKey(UsuarioTopSeat,on_delete=models.CASCADE)
    puestos_d = models.IntegerField(default=4) 
    fecha = models.DateField()
    hora = models.fields.TimeField()
    ruta = models.OneToOneField(Ruta,on_delete=models.SET_NULL,null=True, blank=True)
    vehiculo =models.ForeignKey(Vehiculo,on_delete=models.SET_NULL,null=True, blank=True)
    tarifa = models.IntegerField(default=0)
    enCurso= models.BooleanField(default = False)
    terminado = models.BooleanField(default = False)
    def __str__(self):
        return " ["+str(self.conductor.usuario.username) +"] "+ str(self.ruta)

class Reserva(models.Model):
    id = models.AutoField(primary_key=True)
    pasajero = models.ForeignKey(UsuarioTopSeat,on_delete=models.CASCADE)
    viaje = models.OneToOneField(Viaje,on_delete=models.CASCADE)
    cantidadPuestos = models.IntegerField(default=1)
    estado = models.BooleanField(default=True)
    parada= models.CharField(max_length=254, blank=True, null=True)
    def __str__(self):
        return str(self.viaje) +" {"+self.pasajero.usuario.username +"}"
    
#------------------------Admnistracion--------------------

