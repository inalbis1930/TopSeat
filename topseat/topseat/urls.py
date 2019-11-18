"""

Configuracion de los URL's de la aplicacion "topseat"

Añade ademas los URL's de AdmonCuentas, Viajes, Informativo, Eventos, admin

"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views as topseat_views

app_name='topseat' #Definicion del nombre de la aplicacion para su uso en otros links y Redirects


urlpatterns = [
    url(r'^admin/', admin.site.urls), #Vista de administrador
    url(r'^$', topseat_views.home,name='home'),#Pagina principal de toda la aplicacion
    url(r'^AdmonCuentas/', include('AdmonCuentas.urls', namespace='AdmonCuentas')),#Inclusion de los Urls de la aplicacion de cuentas
    url(r'^Viajes/', include('Viajes.urls', namespace='Viajes')),#Inclusion de los Urls de la aplicacion de cuentas
    url(r'^Informativo/', include('Informativo.urls', namespace='Informativo')),#Inclusion de los Urls de la aplicacion de cuentas
    url(r'^Eventos/', include('Eventos.urls', namespace='Eventos')),#Inclusion de los Urls de la aplicacion de cuentas
]
