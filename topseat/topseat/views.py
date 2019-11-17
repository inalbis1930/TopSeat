from django.http import HttpResponse
from django.shortcuts import render,redirect

def home(request):
    """
        Parametros
        ----------
        request: httprequest
            https://docs.djangoproject.com/en/2.2/ref/request-response/
            Lleva Consigo la informacion de que metodo hace la peticion y con que informacion.
        
        Retorno
        ----------
        Retorna una Página HTML estatica correspondiente al home o pagina principal de la aplicacion.
        
    """
    return render(request,'topseat/home.html')