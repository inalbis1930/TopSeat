from django.shortcuts import render
from AdmonCuentas.Modelo.models import UsuarioTopSeat
from ..Modelo.models import *
from django.contrib.auth.models import User
from django.views import View
# Create your views here.
class FAQView(View):
    def get(self, request, *args, **kwargs):
        a=""
        if request.user.is_authenticated:
            a="baseApp.html"
            datos={'template': a, 'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request),'movil':esMovil(request)}
        else:
            a="base.html"
            datos={'template': a,'movil':esMovil(request)}
        faq=FAQ.objects.all()
        datos['items']=faq
        return render(request,'Informativo/FAQ.html',datos)

def getRol( request):
    a=User.objects.get(username=request.user.username)
    b= UsuarioTopSeat.objects.get(usuario = a)
    if b.rol == 2:
        rol="Conductor"
    else:
        rol="Pasajero"
    return rol

def esMovil(request):
    return request.user_agent.is_mobile
class NovedadView(View):
    def get(self, request, *args, **kwargs):
        a=""
        if request.user.is_authenticated:
            a="baseApp.html"
            datos={'template': a, 'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request),'movil':esMovil(request)}
        else:
            a="base.html"
            datos={'template': a, 'movil':esMovil(request)}
        nov=Novedad.objects.all()
        datos['items']=nov
        return render(request,'Informativo/Novedades.html',datos)
