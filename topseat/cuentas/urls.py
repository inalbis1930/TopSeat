from django.conf.urls import url
from cuentas import views


app_name='cuentas'

urlpatterns = [
    url(r'^$', views.home_cuentas,name='cuentas_home'),
    url(r'^login/', views.login,name='login'),
    url(r'^signup/', views.signup,name='signup'),

]