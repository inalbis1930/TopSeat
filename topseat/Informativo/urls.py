from django.conf.urls import url
from Informativo.Vistas import views

'''
    URLS de la apliccion de informativo, con sus vistas asociadas y respectivos nombres.
'''
app_name='Informativo'

urlpatterns = [
    url(r'^FAQ/', views.FAQView.as_view(),name='FAQ'),
    url(r'^Novedades/', views.NovedadView.as_view(),name='Novedades'),
    url(r'^reporteBug/', views.ReporteBug.as_view(),name='Bug'),
]