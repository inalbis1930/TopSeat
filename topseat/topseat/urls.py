"""

Configuracion de los URL's de la aplicacion "topseat"

Esta contenida las paginas estaticas y las aplicaciones de "cuentas", "aplicacion", "admin"

"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views as topseat_views

app_name='topseat' #Definicion del nombre de la aplicacion para su uso en otros links y Redirects

'''
Para acceder a un link de esta apliacion se debe ralizar de la siguiente manera:
    <app_name>:<namespace>
    Ex. topseat:cuentas
'''

urlpatterns = [
    url(r'^admin/', admin.site.urls), #Vista de administrador
    url(r'^$', topseat_views.home,name='home'),#Pagina principal de toda la aplicacion
    url(r'^cuentas/', include('cuentas.urls', namespace='cuentas')),#Inclusion de los Urls de la aplicacion de cuentas
    url(r'^aplicacion/', include('aplicacion.urls', namespace='aplicacion')),#Inclusion de los Urls de la aplicacion de cuentas
]
