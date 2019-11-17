from django.conf.urls import url
from .Vistas import views


app_name='Eventos'

urlpatterns = [
    url(r'^CrearQueja/$', views.crearQueja.as_view(),name='Crear_Queja'),
    url(r'^CrearSugerencia/$', views.crearSugerencia.as_view(),name='Crear_Sugerencia'),
    url(r'^CrearFalla/$', views.crearFalla.as_view(),name='Crear_Falla'),  
]