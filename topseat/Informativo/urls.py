from django.conf.urls import url
from Informativo import views


app_name='Informativo'

urlpatterns = [
    url(r'^FAQ/', views.FAQPage,name='FAQ'),
    url(r'^Novedades/', views.Novedades,name='Novedades'),
]