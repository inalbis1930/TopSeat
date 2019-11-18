# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import *
from ..Modelo.models import *
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render,redirect
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
            return render(request,'Eventos/home.html',datos)
        else:
             return redirect('AdmonCuentas:AdmonCuentas_home')
    def get(self, request, *args, **kwargs):
        if getRol(request) == "Asis":
            datos={'Q':Queja.objects.filter(respondida=False),'F':Falla.objects.filter(respondida=False),'S':Sugerencia.objects.filter(respondida=False)}
            return render(request,'Eventos/home.html',datos)
        else:
             return redirect('AdmonCuentas:AdmonCuentas_home')
    def dispatch(self, request,*args, **kwargs):
        return super(Ahome, self).dispatch(request,*args, **kwargs)
class SQuejas(View):
    def post(self, request, *args, **kwargs):
        datos={}
        form = responderQueja(data=request.POST)
        if form.is_valid():
            q=Queja.objects.get(pk=request.POST.get('id',''))
            datos= form.save(commit =False)
            if datos.respuesta !="":
                q.respuesta=datos.respuesta
            if datos.respondida ==False:
                q.respondida=True
            q.save()
            request.session['mensaje']='Queja Respondida'
            return redirect('Eventos:Ahome')
        else:
            datos['resp']=form
            datos['q']= Queja.objects.get(pk=request.POST.get('id',''))
            datos['id'] = request.POST.get('id','')  
            datos['error']=form.errors
            return render(request,'Eventos/squeja.html',datos)
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
            if datos.respuesta !="":
                q.respuesta=datos.respuesta
            if datos.respondida ==False:
                q.respondida=True
            q.save()
            request.session['mensaje']='Falla Respondida'
            return redirect('Eventos:Ahome')
        else:
            datos['error']=form.errors
            return render(request,'Eventos:AFallas',datos)

    def get(self, request, *args, **kwargs):
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        form = responderFalla()
        datos['resp']=form
        datos['q']= Falla.objects.get(pk=request.GET.get('id',''))
        datos['id'] = request.GET.get('id','')
        return render(request,'Eventos/sfalla.html',datos)

    def dispatch(self, request,*args, **kwargs):
        return super(SFallas, self).dispatch(request,*args, **kwargs)
class SSugerencias(View):
    def post(self, request, *args, **kwargs):
        datos={}
        form = responderSugerencia(data=request.POST)
        if form.is_valid():
            q=Sugerencia.objects.get(pk=request.POST.get('id',''))
            datos= form.save(commit =False)
            if datos.agradecimiento !="":
                q.agradecimiento=datos.agradecimiento
            if datos.respondida ==False:
                q.respondida=True
            q.save()
            request.session['mensaje']='Sugerencia Respondida'
            return redirect('Eventos:Ahome')
        else:
            datos['error']=form.errors
            return render(request,'Eventos:ASugerencias',datos)

    def get(self, request, *args, **kwargs):
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        form = responderSugerencia()
        datos['resp']=form
        datos['q']= Sugerencia.objects.get(pk=request.GET.get('id',''))
        datos['id'] = request.GET.get('id','')
        return render(request,'Eventos/ssug.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(SSugerencias, self).dispatch(request,*args, **kwargs)

# Create your views here.
@method_decorator(login_required, name='dispatch') 
class crearQueja(View):
    def post(self, request, *args, **kwargs):
        datos = {'usuario': request.user.first_name + " "+request.user.last_name,'rol':getRol(request)}
        queja = crearQuejaF(data=request.POST)
        queja.cliente= UsuarioTopSeat.objects.get(usuario__username=request.user.username)
        print(queja)
        if queja.is_valid():
            queja = form.save(commit = False)
            if queja.viaje == None or queja.descripcion==None or queja.cliente == None :
                datos['error']="Por Favor escriba los campos indicados"
            else:
                queja.save()
                request.session['mensaje'] = 'Queja Creada'
                return redirect('Viajes:Viajes_home')
        else:
            datos['error'] = queja.errors
        return render(request, 'Eventos/cqueja.html', datos)
    def get(self, request, *args, **kwargs):
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        form = crearQuejaF()
        datos['resp']=form
        return render(request,'Eventos/cqueja.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(crearQueja, self).dispatch(request,*args, **kwargs)
        
@method_decorator(login_required, name='dispatch') 
class crearSugerencia(View):
    def post(self, request, *args, **kwargs):
        datos = {'usuario': request.user.first_name + " "+request.user.last_name,'rol':getRol(request)}
        sugerencia = crearSugerenciaF(data=request.POST)
        
        if sugerencia.is_valid():
            sugerencia = sugerencia.save(commit = False)
            sugerencia.cliente= UsuarioTopSeat.objects.get(usuario__username=request.user.username)
            if sugerencia.nombre == None or sugerencia.descripcion==None or sugerencia.motivacion == None :
                datos['error']="Por Favor escriba los campos indicados"
            else:
                sugerencia.save()
                request.session['mensaje'] = 'Sugerencia Enviada'
                request.session['mensaje'] = 'Muchisimas Gracias. De esta manera mejoramos nuestro servicio'
                return redirect('Viajes:Viajes_home')
        else:
            datos['error'] = sugerencia.errors
        return render(request, 'Eventos:Crear_Sugerencia', datos)
    def get(self, request, *args, **kwargs):
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        form = crearSugerenciaF()
        datos['resp']=form
        return render(request,'Eventos/csug.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(crearSugerencia, self).dispatch(request,*args, **kwargs)

@method_decorator(login_required, name='dispatch') 
class crearFalla(View):
    def post(self, request, *args, **kwargs):
        datos = {'usuario': request.user.first_name + " "+request.user.last_name,'rol':getRol(request)}
        falla = crearFallaF(data=request.POST)
        if falla.is_valid():
            falla = falla.save(commit = False)
            falla.cliente= UsuarioTopSeat.objects.get(usuario__username=request.user.username)
            if falla.secuencia == None or falla.contexto == None :
                datos['error']="Por Favor escriba los campos indicados"
            else:
                falla.save()
                request.session['mensaje'] = 'Falla Creada'
                return redirect('Viajes:Viajes_home')
        else:
            datos['error'] = falla.errors
        return render(request, 'Evento:Crear_Falla', datos)
    def get(self, request, *args, **kwargs):
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        form = crearFallaF()
        datos['resp']=form
        return render(request,'Eventos/cfalla.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(crearFalla, self).dispatch(request,*args, **kwargs)
class reportarMayor(View):
    def post(self, request, *args, **kwargs):
        datos={}
        form = reportarEventoMayor(data=request.POST)
        if form.is_valid():
            q=Queja.objects.get(pk=request.POST.get('id',''))
            q.respondida=True
            q.save()
            datos= form.save(commit =False)
            datos.queja=q
            datos.save()
            request.session['mensaje']='Convertido a Evento Mayor'
            return redirect('Eventos:Ahome')
        else:
            datos['error']=form.errors
            return render(request,'Eventos:RM',datos)

    def get(self, request, *args, **kwargs):
        datos={}
        form = reportarEventoMayor()
        datos['resp']=form
        datos['q']= Queja.objects.get(pk=request.GET.get('id',''))
        datos['id'] = request.GET.get('id','')
        datos['em']=True
        return render(request,'Eventos/squeja.html',datos)

    def dispatch(self, request,*args, **kwargs):
        return super(reportarMayor, self).dispatch(request,*args, **kwargs)
def esMovil(request):
    return request.user_agent.is_mobile