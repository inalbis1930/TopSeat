from django import forms
from django.db import models
from django_google_maps import fields as map_fields
from Viajes.Modelo.models import *
from AdmonCuentas.Modelo.models import *
# Create your models here.

class Queja(models.Model):
    id = models.AutoField(primary_key = True)
    viaje = models.ForeignKey(Viaje,on_delete=models.CASCADE)
    clienteAfectado = models.ForeignKey(UsuarioTopSeat,on_delete=models.CASCADE,related_name='afectado')
    clienteAcusado = models.ForeignKey(UsuarioTopSeat,on_delete=models.CASCADE,related_name='acusado')
    descripcion = models.CharField(max_length = 300)
    respuesta=models.CharField(max_length = 300, null=True,blank=True)
    def __str__(self):
        return str.viaje+str.cliente + "[ "+ str.descripcion + "]"

class Sugerencia(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 50)
    motivacion = models.CharField(max_length = 300)
    descripcion = models.CharField(max_length = 300)
    cliente = models.ForeignKey(UsuarioTopSeat,on_delete=models.CASCADE)
    agradecimiento=models.CharField(max_length = 300, null=True,blank=True)
    def __str__(self):
        return str.descripcion + " " + str.motivacion

class Falla(models.Model):
    id = models.AutoField(primary_key = True)
    secuencia = models.CharField(max_length = 300)
    contexto = models.CharField(max_length = 300)
    cliente = models.ForeignKey(UsuarioTopSeat,on_delete=models.CASCADE)
    respuesta=models.CharField(max_length = 300, null=True,blank=True)
    def __str__(self):
        return str.secuencia + " " + str.contexto
class EventoMayor(models.Model):
     id = models.AutoField(primary_key = True)
     queja=models.ForeignKey(Queja,on_delete=models.CASCADE)
     justificacion=models.CharField(max_length = 500)
