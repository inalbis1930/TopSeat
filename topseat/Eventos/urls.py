from django.conf.urls import url
from Eventos import views


app_name='Eventos'

urlpatterns = [
    #url(r'^$', views.Eventos_home,name='Eventos_home'),
    url(r'^CrearQueja/$', views.crearQueja,name='Crear_Queja'),
    url(r'^CrearSugerencia/$', views.crearSugerencia,name='Crear_Sugerencia'),
    url(r'^CrearFalla/$', views.crearFalla,name='Crear_Falla'),  
]