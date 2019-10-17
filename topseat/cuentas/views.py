# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout
from .forms import *
from .models import *

# Create your views here.

def home_cuentas(request):
    return render(request,'cuentas/home.html')

def signup_v(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        form1 = ProfileForm(request.POST)
        if verificar_Correo(form1):
            if form.is_valid():
                usuarioAct= form.save()
                perfil = form1.save(commit=False)
                perfil.usuario=usuarioAct
                perfil.save()
                login(request,usuarioAct)
                if perfil.rol == 1:
                    return redirect('aplicacion:aplicacion_home')#('appname:linkname')
                else:
                    return redirect('aplicacion:registro_vehiculo')
            else:
                return  render(request,'cuentas/signup.html',{'sgForm':form,'prForm':form1,'error':form.errors})
        else:
            return  render(request,'cuentas/signup.html',{'sgForm':form,'prForm':form1,'error':"Por favor Ingrese correo institucional de la PUJ"})
    else:
        form = UserCreationForm()
        form1=ProfileForm()
    return render(request,'cuentas/signup.html',{'sgForm':form,'prForm':form1})

def verificar_Correo(form):
    perfil =form.save(commit=False)
    correo= perfil.correo
    partes= correo.split('@')
    if partes[1] != 'javeriana.edu.co':
        return False
    else:
        return True
    

def login_v(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            if 'next' in request.POST:
                return redirect (request.POST.get('next'))
            return redirect('aplicacion:aplicacion_home')#('appname:linkname')
    else:
        form = AuthenticationForm()
    return render(request,'cuentas/login.html',{'lgForm':form})
      
def logout_v(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def cambiarRol(request):
    if request.method == 'POST':
        a=User.objects.get(username=request.user.username)
        b= Perfil.objects.get(usuario = a)
        if b.rol ==2:
           b.rol=1
           r='aplicacion:pasajero'
        else:
           b.rol=2
           r='aplicacion:conductor'
        b.save()
        return redirect("aplicacion:aplicacion_home")

#def actualizarPerfil(request):


