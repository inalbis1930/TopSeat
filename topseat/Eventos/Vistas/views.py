# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import *
from ..Modelo.models import *
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def getRol(request):
    a=User.objects.get(username=request.user.username)
    b= UsuarioTopSeat.objects.get(usuario = a)
    if b.rol == 2:
        rol="Conductor"
    elif b. rol == 1:
        rol="Pasajero"
    else:
        rol="Asis"
    return rol
@method_decorator(login_required, name='dispatch') 
class Ahome(View):
    def post(self, request, *args, **kwargs):
        if getRol(request) == "Asis":
            datos={'Q':Queja.objects.filter(respondida=False),'F':Falla.objects.filter(respondida=False),'S':Sugerencia.objects.filter(respondida=False)}
            print(datos['F'])
            return render(request,'Eventos/home.html',datos)
        else:
             return redirect('AdmonCuentas:AdmonCuentas_home')
    def get(self, request, *args, **kwargs):
        if getRol(request) == "Asis":
            datos={'Q':Queja.objects.filter(respondida=False),'F':Falla.objects.filter(respondida=False),'S':Sugerencia.objects.filter(respondida=False)}
            print(datos['F'])
            return render(request,'Eventos/home.html',datos)
        else:
             return redirect('AdmonCuentas:AdmonCuentas_home')
    def dispatch(self, request,*args, **kwargs):
        return super(Ahome, self).dispatch(request,*args, **kwargs)
class SQuejas(View):
    def post(self, request, *args, **kwargs):
        form = responderQueja(data=request.POST)
        if form.is_valid():
            q=Queja.objects.get(pk=request.POST.get('id',''))
            datos= form.save(commit =False)
            if datos.viaje !=None:
                q.viaje=datos.viaje
            if datos.clienteAfectado !=None:
                q.clienteAfectado=datos.clienteAfectado
            if datos.clienteAcusado !=None:
                q.clienteAcusado=datos.clienteAcusado
            if datos.descripcion !=None:
                q.descripcion=datos.descripcion
            if datos.respuesta !="":
                q.respuesta=datos.respuesta
            if datos.respondida !=False:
                q.respondida=datos.respondida
            q.save()
            request.session['mensaje']='Queja Respondida'
            return redirect('Eventos:Ahome')
        else:
            datos['error']=form.errors
            return render(request,'Viajes/nuevoViaje.html',datos)
    def get(self, request, *args, **kwargs):
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        form = responderQueja()
        datos['resp']=form
        datos['q']= Queja.objects.get(pk=request.GET.get('id',''))
        datos['id'] = request.GET.get('id','')
        return render(request,'Eventos/squeja.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(SQuejas, self).dispatch(request,*args, **kwargs)
class SFallas(View):
    def post(self, request, *args, **kwargs):
        datos={}
        form = responderFalla(data=request.POST)
        if form.is_valid():
            q=Falla.objects.get(pk=request.POST.get('id',''))
            datos= form.save(commit =False)
            if datos.secuencia !="":
                q.secuencia=datos.secuencia
            if datos.contexto !="":
                q.contexto=datos.contexto
            if datos.cliente !=None:
                q.cliente=datos.cliente
            if datos.respuesta !="":
                q.respuesta=datos.respuesta
            if datos.respondida ==False:
                q.respondida=True
            q.save()
            request.session['mensaje']='Falla Respondida'
            return redirect('Eventos:Ahome')
        else:
            datos['error']=form.errors
            return render(request,'Eventos/home.html',datos)

    def get(self, request, *args, **kwargs):
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        form = responderFalla()
        datos['resp']=form
        datos['q']= Falla.objects.get(pk=request.GET.get('id',''))
        datos['id'] = request.GET.get('id','')
        return render(request,'Eventos/squeja.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(SFallas, self).dispatch(request,*args, **kwargs)
class SSugerencias(View):
    def post(self, request, *args, **kwargs):
        return render(request,'Eventos/home.html')
    def get(self, request, *args, **kwargs):
        return render(request,'Eventos/home.html')
    def dispatch(self, request,*args, **kwargs):
        return super(SSugerencias, self).dispatch(request,*args, **kwargs)

# Create your views here.
@method_decorator(login_required, name='dispatch') 
class crearQueja(View):
    def post(self, request, *args, **kwargs):
        datos = {'usuario': request.user.first_name + " "+request.user.last_name,'rol':getRol(request)}
        queja = crearQueja(request.user, data=request.POST)
        datos['QForm'] = form
        if form.is_valid():
            queja = form.save(commit = False)
            if queja.viaje == None or queja.descripcion==None or queja.cliente == None :
                datos['error']="Por Favor escriba los campos indicados"
            else:
                queja.save()
                request.session['mensaje'] = 'Queja Creada'
                return redirect('Viajes:Viajes_home')
        else:
            datos['error'] = form.errors
        return render(request, 'Eventos:crear_queja', datos)
    def dispatch(self, request,*args, **kwargs):
        return super(crearQueja, self).dispatch(request,*args, **kwargs)
        
@method_decorator(login_required, name='dispatch') 
class crearSugerencia(View):
    def post(self, request, *args, **kwargs):
        datos = {'usuario': request.user.first_name + " "+request.user.last_name,'rol':getRol(request)}
        sugerencia = crearSugerencia(request.user, data=request.POST)
        datos['QForm'] = form
        if form.is_valid():
            sugerencia = form.save(commit = False)
            if sugerencia.nombre == None or sugerencia.descripcion==None or sugerencia.motivacion == None :
                datos['error']="Por Favor escriba los campos indicados"
            else:
                sugerencia.save()
                request.session['mensaje'] = 'Sugerencia Enviada'
                request.session['mensaje'] = 'Muchisimas Gracias. De esta manera mejoramos nuestro servicio'
                return redirect('Viajes:Viajes_home')
        else:
            datos['error'] = form.errors
        return render(request, 'Eventos:Crear_Sugerencia', datos)
    def dispatch(self, request,*args, **kwargs):
        return super(crearSugerencia, self).dispatch(request,*args, **kwargs)

@method_decorator(login_required, name='dispatch') 
class crearFalla(View):
    def post(self, request, *args, **kwargs):
        datos = {'usuario': request.user.first_name + " "+request.user.last_name,'rol':getRol(request)}
        if request.method == 'POST':
            falla = crearFalla(request.user, data=request.POST)
            datos['QForm'] = form
            if form.is_valid():
                falla = form.save(commit = False)
                if falla.secuencia == None or falla.contexto == None :
                    datos['error']="Por Favor escriba los campos indicados"
                else:
                    falla.save()
                    request.session['mensaje'] = 'Falla Creada'
                    return redirect('Viajes:Viajes_home')
            else:
                datos['error'] = form.errors
        return render(request, 'Evento:Crear_Falla', datos)
    def dispatch(self, request,*args, **kwargs):
        return super(crearFalla, self).dispatch(request,*args, **kwargs)

def esMovil(request):
    return request.user_agent.is_mobile