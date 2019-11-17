from django import forms
from django.db import models
from django_google_maps import fields as map_fields

# Create your models here.

class Queja(models.Model):
    id = models.AutoField(primary_key = True)
    viaje = models.IntegerField(default = 6)
    cliente = models.CharField(max_length = 60)
    descripcion = models.CharField(max_length = 300)
    def __str__(self):
        return str.viaje+str.cliente + "[ "+ str.descripcion + "]"

class Sugerencia(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 50)
    motivacion = models.CharField(max_length = 300)
    descripcion = models.CharField(max_length = 300)
    def __str__(self):
        return str.descripcion + " " + str.motivacion

class Falla(models.Model):
    id = models.AutoField(primary_key = True)
    secuencia = models.CharField(max_length = 300)
    contexto = models.CharField(max_length = 300)
    def __str__(self):
        return str.secuencia + " " + str.contexto
