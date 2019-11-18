from django.conf.urls import url
from AdmonCuentas.Vistas import views

'''
    Todos los urls y referencias a vistas con nombres de la aplicacion de AdmonCuentas
'''
app_name='AdmonCuentas'

urlpatterns = [
    url(r'^$', views.home_AdmonCuentas.as_view(),name='AdmonCuentas_home'),
    url(r'^login/', views.login_v.as_view(),name='login'),
    url(r'^signup/', views.signup_v.as_view(),name='signup'),
    url(r'^logout/', views.logout_v.as_view(),name='logout'),
	url(r'^cambiar/', views.cambiarRol.as_view(),name='cambiar'),
    url(r'^editarPerfil/', views.actualizarPerfil.as_view(),name='editar_perfil'),
    url(r'^actualizarContrasena/', views.actualizarContrasena.as_view(),name='actualizarContrasena'),
    url(r'^eliminarPerfil/', views.eliminarPerfil.as_view(),name='eliminarPerfil'),
    url(r'^ReporteViajes/', views.ReporteViajes.as_view(),name='ReporteViajes'),
    url(r'^registro-v/$', views.registrov.as_view(),name='registro_vehiculo'),
]