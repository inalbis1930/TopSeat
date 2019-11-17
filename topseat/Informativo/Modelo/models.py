from django.db import models
from Eventos.Modelo.models import *
#from Eventos import Bug
# Create your models here.
class FAQ(models.Model):
    id= models.AutoField(primary_key=True)
    pregunta = models.CharField(max_length=100,default='¿?')
    solucion= models.CharField(max_length=300,default='')
    def __str__(self):
        return self.pregunta

class Bug(models.Model):
    id= models.AutoField(primary_key=True)
    estado=models.CharField(max_length=40,default='')
    justificacion = models.CharField(max_length=700,default='')
    falla=models.OneToOneField(Falla,on_delete=models.CASCADE,default='')
    def __str__(self):
        return self.justificacion

class Novedad(models.Model):
    id= models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100,default='')
    descripcion= models.CharField(max_length=500,default='')
    bug=models.OneToOneField(Bug,on_delete=models.CASCADE, blank=True,default='')
    def __str__(self):
        return self.nombre

