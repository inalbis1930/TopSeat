from django.conf.urls import url
from Informativo.Vistas import views


app_name='Informativo'

urlpatterns = [
    url(r'^FAQ/', views.FAQPage,name='FAQ'),
    url(r'^Novedades/', views.NovedadesPage,name='Novedades'),
]