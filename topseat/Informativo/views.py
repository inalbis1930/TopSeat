from django.shortcuts import render
from AdmonCuentas.models import UsuarioTopSeat
from .models import *
from django.contrib.auth.models import User
# Create your views here.
def FAQPage(request):
    a=""
    if request.user.is_authenticated:
        a="baseApp.html"
    else:
        a="base.html"
    faq=FAQ.objects.all()
    datos={'template': a, 'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request),'movil':esMovil(request), 'items':faq}
    return render(request,'Informativo/FAQ.html',datos)
def getRol(request):
    a=User.objects.get(username=request.user.username)
    b= UsuarioTopSeat.objects.get(usuario = a)
    if b.rol == 2:
        rol="Conductor"
    else:
        rol="Pasajero"
    return rol

def esMovil(request):
    return request.user_agent.is_mobile

def NovedadesPage(request):
    a=""
    if request.user.is_authenticated:
        a="baseApp.html"
    else:
        a="base.html"
    faq=Novedad.objects.all()
    datos={'template': a, 'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request),'movil':esMovil(request), 'items':faq}
    return render(request,'Informativo/Novedades.html',datos)
