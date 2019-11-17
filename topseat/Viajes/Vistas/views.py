# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from ..Modelo.models import *
from django_google_maps import widgets as map_widgets
from AdmonCuentas.Modelo.models import UsuarioTopSeat
from django.contrib.auth.models import User
from django.http import HttpResponse

@login_required(login_url="/AdmonCuentas/login/")
def Viajes_home(request):
    datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request),'movil':esMovil(request)}
    if getRol(request) == "Conductor":
        if request.method == 'POST':
            origen = request.POST.get("origen","")
            fin = request.POST.get("fin","")
            datos['inicio']=str(origen)
            datos['fin']=str(fin)
            return render(request,'Viajes/verMapa.html',datos)
        else:
            v=Viaje.objects.filter(conductor__usuario =request.user)
            datos['viajes']=v
            r= Reserva.objects.filter(viaje__conductor__usuario=request.user,estado=True)
            datos['reservas']=r
            if 'mensaje' in request.session and request.session['mensaje'] != None:
                datos['mensaje']=request.session['mensaje']
                request.session['mensaje']= None
            return render(request,'Viajes/conductor.html',datos)
    else:
        if request.method == 'POST':
            origen = request.POST.get("origen","")
            fin = request.POST.get("fin","")
            datos['inicio']=str(origen)
            datos['fin']=str(fin)
            return render(request,'Viajes/verMapa.html',datos)
        else:
            v=Viaje.objects.filter(puestos_d__gte=1).exclude(conductor__usuario=request.user)
            datos['viajes']=v
            r= Reserva.objects.filter(pasajero__usuario = request.user,estado=True)
            datos['reservas']=r
            if 'mensaje' in request.session and request.session['mensaje'] != None:
                datos['mensaje']=request.session['mensaje']
                request.session['mensaje']= None
            return render (request,'Viajes/pasajero.html',datos)

def esMovil(request):
    return request.user_agent.is_mobile

@login_required(login_url="/AdmonCuentas/login/")
def registrov(request):
    datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
    if request.method == 'POST':
        form = registrarVehiculo_f(request.POST)
        if form.is_valid():
            a=User.objects.get(username=request.user.username)
            vehiculo = form.save(commit = False)
            vehiculo.dueno = a
            vehiculo.save()
            request.session['mensaje']='Vehiculo Registrado'
            return redirect('Viajes:Viajes_home')#('appname:linkname')
    else:
        v= Vehiculo.objects.filter(dueno=request.user)
        if len(v) ==0:
            datos['error']="Por favor registre un vehiculo primero"
        form = registrarVehiculo_f()
        datos['rvForm']=form
    return render(request,'Viajes/registroVehiculo.html',datos)
       

def getRol(request):
    a=User.objects.get(username=request.user.username)
    b= UsuarioTopSeat.objects.get(usuario = a)
    if b.rol == 2:
        rol="Conductor"
    else:
        rol="Pasajero"
    return rol


@login_required(login_url="/AdmonCuentas/login/")
def crearViaje(request):
    datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
    if request.method == 'POST':
        form = form_crearViaje(request.user,data=request.POST)
        formruta=form_CrearRuta(data=request.POST)
        datos['nvForm']=form
        datos['rtForm']=formruta
        if form.is_valid():
            viaje=form.save(commit =False)
            if viaje.vehiculo == None:
                datos['error']="Por Favor eliga un Vehiculo"
            else:
                ruta=formruta.save()
                viaje.ruta=ruta
                viaje.conductor=UsuarioTopSeat.objects.get(usuario=request.user)
                viaje.save()
                request.session['mensaje']='Viaje Creado'
                return redirect('Viajes:Viajes_home')
        else:
            datos['error']=form.errors
            render(request,'Viajes/nuevoViaje.html',datos)
    else:
        v= Vehiculo.objects.filter(dueno=request.user)
        if len(v) ==0:
            return redirect('Viajes:registro_vehiculo')
        form = form_crearViaje(request.user)
        formruta=form_CrearRuta()
        datos['nvForm']=form
        datos['rtForm']=formruta
    return render(request,'Viajes/nuevoViaje.html',datos)

@login_required(login_url="/AdmonCuentas/login/")
def verMapa(request):
    datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
    v=Vehiculo.objects.filter(dueno=request.user)
    if len(v):
        datos['vehiculos']=v
    if request.method == 'POST':
        print(request)
    return render(request,'Viajes/verMapa.html',datos)

@login_required(login_url="/AdmonCuentas/login/")    
def eliminarViaje(request):
    if request.method == 'POST':
        viaje =Viaje.objects.get(id=request.POST.get('id',''))
        viaje.delete()
        request.session['mensaje']='Viaje Eliminado'
        return redirect('Viajes:Viajes_home')

@login_required(login_url="/AdmonCuentas/login/")
def editarViaje(request):
    datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
    if request.method == 'POST':
        form = modificarViaje(data=request.POST)
        formruta=modificarRuta(data=request.POST)
        if form.is_valid():
            viaje=Viaje.objects.get(pk=request.POST.get('id',''))
            datos= form.save(commit =False)
            datosruta=formruta.save(commit =False)
            ruta=viaje.ruta
            if datosruta.inicio !="":
                ruta.inicio=datosruta.inicio
            if datosruta.fin !="":
                ruta.fin=datosruta.fin
            if datos.puestos_d != None:
                viaje.puestos_d=datos.puestos_d
            if datos.fecha != None:
                viaje.fecha=datos.fecha
            if datos.hora != None:
                viaje.hora=datos.hora
            if datos.vehiculo != None:
                viaje.vehiculo=datos.vehiculo
            if datos.tarifa != None:
                viaje.tarifa=datos.tarifa
            ruta.save()
            viaje.save()
            request.session['mensaje']='Viaje Actualizado'
            return redirect('Viajes:Viajes_home')
        else:
            datos['error']=form.errors
            render(request,'Viajes/nuevoViaje.html',datos)
    else:
        form = modificarViaje()
        formruta=modificarRuta()
        datos['nvForm']=form
        datos['rtForm']=formruta
        datos['id'] = request.GET.get('id','')
    return render(request,'Viajes/editarViaje.html',datos)

@login_required(login_url="/AdmonCuentas/login/")
def confirmarReserva(request):
    datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
    if request.method =='POST':
        viaje=Viaje.objects.get(pk=request.POST.get('id',''))
        datos['inicio']=viaje.ruta.inicio
        datos['fin']=viaje.ruta.fin
        datos['viaje']=viaje
        form = f_confirmarReserva(data=request.POST) 
        datos['crForm']=form
        if form.is_valid():
            data= form.save(commit=False)
            cant=int(data.cantidadPuestos)
            if cant< 1 or cant > viaje.puestos_d:
                datos['error']="Por favor ingrese una cantidad de puestos Valida"
                render(request,'Viajes/confirmarReserva.html',datos)
            else:
                r= Reserva()
                r.pasajero = UsuarioTopSeat.objects.get(usuario=request.user)
                r.viaje=viaje
                r.cantidadPuestos = cant
                viaje.puestos_d -= cant
                r.save()
                viaje.save()
                request.session['mensaje']='Reserva Realizada'
                return redirect('Viajes:Viajes_home')
        else:
            datos['error']=form.errors
            render(request,'Viajes/confirmarReserva.html',datos)
    else:
        viaje=Viaje.objects.get(pk=request.GET.get('id',''))
        datos['inicio']=viaje.ruta.inicio
        datos['fin']=viaje.ruta.fin
        form = f_confirmarReserva()
        datos['crForm']=form
        datos['viaje']=viaje
    return render(request,'Viajes/confirmarReserva.html',datos)

def eliminarReserva(request):
    if request.method == 'POST':
        r = Reserva.objects.get(pk=request.POST.get('id',''))
        cant = r.cantidadPuestos
        v= Viaje.objects.get(pk=r.viaje.id)
        v.puestos_d +=cant
        v.save()
        r.delete()
        request.session['mensaje']='Reserva Eliminada'
        return redirect('Viajes:Viajes_home')


def IniciarViaje(request):
    datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
    if request.method == 'POST':
        v= Viaje.objects.get(pk=request.POST.get('id',''))
        v.enCurso= True
        v.save()
        return redirect('Viajes:Viajes_home')
    else:
        v= Viaje.objects.get(pk=request.GET.get('id',''))
        datos['viaje']= v
        datos['inicio']=v.ruta.inicio
        datos['fin']=v.ruta.fin
        r = Reserva.objects.filter(viaje=v)
        datos['reservas']=r
    return render(request,'Viajes/IniciarViaje.html',datos)


