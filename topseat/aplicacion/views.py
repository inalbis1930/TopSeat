# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django_google_maps import widgets as map_widgets
from cuentas.models import Perfil
from django.contrib.auth.models import User
from django.http import HttpResponse

@login_required(login_url="/cuentas/login/")
def aplicacion_home(request):
    datos={'usuario':request.user.username,'rol':getRol(request)}
    if getRol(request) == "Conductor":
        if request.method == 'POST':
            origen = request.POST.get("origen","")
            fin = request.POST.get("fin","")
            datos['inicio']=str(origen)
            datos['fin']=str(fin)
            return render(request,'aplicacion/verMapa.html',datos)
        else:
            v=Viaje.objects.filter(conductor =request.user)
            datos['viajes']=v
            return render(request,'aplicacion/conductor.html',datos)
    else:
        if request.method == 'POST':
            origen = request.POST.get("origen","")
            fin = request.POST.get("fin","")
            datos['inicio']=str(origen)
            datos['fin']=str(fin)
            return render(request,'aplicacion/verMapa.html',datos)
        else:
            v=Viaje.objects.filter(puestos_d__gte=0)
            datos['viajes']=v
            return render (request,'aplicacion/pasajero.html',datos)

@login_required(login_url="/cuentas/login/")
def registrov(request):
    datos={'usuario':request.user.username,'rol':getRol(request)}
    if request.method == 'POST':
        form = registrarVehiculo_f(request.POST)
        if form.is_valid():
            a=User.objects.get(username=request.user.username)
            vehiculo = form.save(commit = False)
            vehiculo.dueno = a
            vehiculo.save()
            return redirect('aplicacion:aplicacion_home')#('appname:linkname')
    else:
        form = registrarVehiculo_f()
        datos['rvForm']=form
    return render(request,'aplicacion/registroVehiculo.html',datos)
       

def getRol(request):
    a=User.objects.get(username=request.user.username)
    b= Perfil.objects.get(usuario = a)
    if b.rol == 2:
        rol="Conductor"
    else:
        rol="Pasajero"
    return rol


@login_required(login_url="/cuentas/login/")
def crearViaje(request):
    datos={'usuario':request.user.username,'rol':getRol(request)}
    if request.method == 'POST':
        form = form_crearViaje(data=request.POST)
        formruta=form_CrearRuta(data=request.POST)
        if form.is_valid():
            viaje=form.save(commit =False)
            ruta=formruta.save()
            viaje.ruta=ruta
            viaje.conductor=request.user
            viaje.save()
            return redirect('aplicacion:aplicacion_home')
        else:
            datos['error']=form.errors
            render(request,'aplicacion/nuevoViaje.html',datos)
    else:
        form = form_crearViaje()
        formruta=form_CrearRuta()
        datos['nvForm']=form
        datos['rtForm']=formruta
    return render(request,'aplicacion/nuevoViaje.html',datos)


def verMapa(request):
    datos={'usuario':request.user.username,'rol':getRol(request)}
    v=Vehiculo.objects.filter(dueno=request.user)
    print("ENTRAAA")
    if len(v):
        datos['vehiculos']=v
    if request.method == 'POST':
        print(request)
    return render(request,'aplicacion/verMapa.html',datos)