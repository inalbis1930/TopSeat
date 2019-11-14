from django.conf.urls import url
from aplicacion import views


app_name='aplicacion'

urlpatterns = [
    url(r'^$', views.aplicacion_home,name='aplicacion_home'),
    url(r'^regisro-v/$', views.registrov,name='registro_vehiculo'),
    url(r'^crearViaje/$', views.crearViaje,name='crearViaje'),
    url(r'^verMapa/$', views.verMapa,name='verMapa'),
    url(r'^eliminarViaje/$', views.eliminarViaje,name='eliminarViaje'),
    url(r'^editarViaje/$', views.editarViaje,name='editarViaje'),
    url(r'^confirmarReserva/$', views.confirmarReserva,name='confirmarReserva'),
    url(r'^eliminarReserva/$', views.eliminarReserva,name='eliminarReserva'),
    
]