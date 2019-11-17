# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import *
from ..Modelo.models import *
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
        return super(ReporteViajes, self).dispatch(request,*args, **kwargs)
        
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
        return super(ReporteViajes, self).dispatch(request,*args, **kwargs)

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
        return super(ReporteViajes, self).dispatch(request,*args, **kwargs)

def esMovil(request):
    return request.user_agent.is_mobile