from django.conf.urls import url
from Informativo.Vistas import views


app_name='Informativo'

urlpatterns = [
    url(r'^FAQ/', views.FAQView.as_view(),name='FAQ'),
    url(r'^Novedades/', views.NovedadView.as_view(),name='Novedades'),
]