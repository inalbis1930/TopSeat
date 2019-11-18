from django import forms
from django.db import models
from django_google_maps import fields as map_fields
from Viajes.Modelo.models import *
from AdmonCuentas.Modelo.models import *

'''
    Tabla en la base de datos de una queja, asocuada a un viaje, dos clientes, y tiene como informacion complementaria 
    una descripcion y una posible respuesta
'''

class Queja(models.Model):
    id = models.AutoField(primary_key = True)
    viaje = models.ForeignKey(Viaje,on_delete=models.CASCADE)
    clienteAfectado = models.ForeignKey(UsuarioTopSeat,on_delete=models.CASCADE,related_name='afectado')
    clienteAcusado = models.ForeignKey(UsuarioTopSeat,on_delete=models.CASCADE,related_name='acusado')
    descripcion = models.CharField(max_length = 300)
    respuesta=models.CharField(max_length = 300, null=True,blank=True)
    respondida= models.BooleanField(default=False)
    def __str__(self):
        return str(self.viaje)+" "+str(self.clienteAfectado) + "[ "+ self.descripcion + "]"
'''
    Tabla en la base de datos de una Sugerencia, asociado a un viaje y tiene informacion complementaria como ayuda.
'''
class Sugerencia(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 50)
    motivacion = models.CharField(max_length = 300)
    descripcion = models.CharField(max_length = 300)
    cliente = models.ForeignKey(UsuarioTopSeat,on_delete=models.CASCADE)
    agradecimiento=models.CharField(max_length = 300, null=True,blank=True)
    respondida= models.BooleanField(default=False)
    def __str__(self):
        return self.descripcion + " " + self.motivacion
'''
    Tabla en la base de datos de una Sugerencia, asociado a un viaje y tiene informacion complementaria como ayuda.
'''
class Falla(models.Model):
    id = models.AutoField(primary_key = True)
    secuencia = models.CharField(max_length = 300)
    contexto = models.CharField(max_length = 300)
    cliente = models.ForeignKey(UsuarioTopSeat,on_delete=models.CASCADE)
    respuesta=models.CharField(max_length = 300, null=True,blank=True)
    respondida= models.BooleanField(default=False)
    def __str__(self):
        return self.secuencia + " " + self.contexto
'''
    Tabla en la base de datos de un evento mayor, asociada a una queja, y una justificacion de por que es un evento mayor

'''
class EventoMayor(models.Model):
    id = models.AutoField(primary_key = True)
    queja=models.ForeignKey(Queja,on_delete=models.CASCADE)
    justificacion=models.CharField(max_length = 500)
    def __str__(self):
        return str(self.queja)
