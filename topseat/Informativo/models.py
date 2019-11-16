from django.db import models
#from Eventos import Bug
# Create your models here.
class FAQ(models.Model):
    id= models.AutoField(primary_key=True)
    pregunta = models.CharField(max_length=100,default='¿?')
    solucion= models.CharField(max_length=300,default='')
    def __str__(self):
        return self.pregunta

class Novedad(models.Model):
    id= models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100,default='')
    descripcion= models.CharField(max_length=500,default='')
    #bug=models.OneToOneField(Bug,on_delete=models.CASCADE, blank=True)
    def __str__(self):
        return self.nombre