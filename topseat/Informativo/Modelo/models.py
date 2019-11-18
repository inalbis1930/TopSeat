from django.db import models
from Eventos.Modelo.models import *


'''
    Informacion de interes para el cliente, preguntas que pueden ser pensadas por el cliente con sus respectivas respuestas por 
    parte del equipo desarrollador
'''
class FAQ(models.Model):
    id= models.AutoField(primary_key=True)
    pregunta = models.CharField(max_length=100,default='¿?')
    solucion= models.CharField(max_length=300,default='')
    def __str__(self):
        return self.pregunta

'''
    Problema en el funcionamiento del sistema, asociado a una falla con un comportamiento conocido.
'''
class Bug(models.Model):
    id= models.AutoField(primary_key=True)
    estado=models.BooleanField(default=False)
    justificacion = models.CharField(max_length=700,default='')
    falla=models.OneToOneField(Falla,on_delete=models.CASCADE,default='')
    def __str__(self):
        return self.justificacion

'''
    En caso de que el bug se arregl o tenga alguna clase de actualizacion
    debe ser reportado por medio de una novedad.
'''
class Novedad(models.Model):
    id= models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100,default='')
    descripcion= models.CharField(max_length=500,default='')
    bug=models.OneToOneField(Bug,on_delete=models.CASCADE, blank=True,default='')
    def __str__(self):
        return self.nombre

