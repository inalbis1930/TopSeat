from __future__ import unicode_literals
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm,PasswordChangeForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout,update_session_auth_hash
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from Viajes.models import *

'''
    Vistas de la aplicacion de AdmonCuentas.
    Esta aplicacion hace el manejo de las AdmonCuentas, tanto creacion, modificacion, eliminacion, cerrar sesion e ingresar al sistema.
    Todas las vistas tienen parametro request 
    
    Parametros
    ----------
    request: httprequest
        https://docs.djangoproject.com/en/2.2/ref/request-response/
        Lleva Consigo la informacion de que metodo hace la peticion y con que informacion.
    
    Esta peticion puede ser de dos metodos
        GET: 
            Retorna la vista de la pagina
        POST:
            Verifica la informacion que trae dentro de la peticion, si es valida redirige a la pagina respectiva
            si no es valida entonces vuelve e a retornar la misma pagina.
'''

def home_AdmonCuentas(request):
    return render(request,'AdmonCuentas/home.html')


'''
    Esta funcion controla el registro de un nuevo cliente.
    
    Parametros
    ----------
    request: httprequest
        https://docs.djangoproject.com/en/2.2/ref/request-response/
        Lleva Consigo la informacion de que metodo hace la peticion y con que informacion.
    
    Primero verifica que clase de metodo trae la peticion (GET o POST).
    
    POST:
        En caso de que sea un metodo de POST, se extrae la informacion de los formularios. 
        Se verifica que la informacion del formulario de crear usuario sea valida.
        En caso de que lo sea, se guarda tanto el Usuario como el Perfil (Models.py)
        Por ultimo lo ingresa al sistema
    GET:
        Crea los formularios de Usuario y Perfil,
        los envia por medio del diccionario de datos que puede ser enviado como tercer parametro a la funcion
        render()
    
    Retorno
    ----------
    *Si el metodo es POST y el formulario es valido
    redirect()
        Si el Rol es Pasajero aplicacion_home
        Si el Rol es Conductor registro_vehiculo
    *Si el metodo es Get o el formulario es Invalido
    render()
        Lleva consigo los formularios para el registro.         
'''
def signup_v(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        form1 = ProfileForm(request.POST)
        if verificar_Correo(form1):
            if form.is_valid():
                usuarioAct= form.save()
                perfil = form1.save(commit=False)
                perfil.usuario=usuarioAct
                perfil.save()
                usuarioAct.first_name = request.POST.get('Nombre','')
                usuarioAct.last_name =request.POST.get('Apellido','')
                usuarioAct.email= perfil.correo
                usuarioAct.save()
                login(request,usuarioAct)
                if perfil.rol == 1:
                    return redirect('Viajes:Viajes_home')
                else:
                    return redirect('Viajes:registro_vehiculo')
            else:
                return  render(request,'AdmonCuentas/signup.html',{'sgForm':form,'prForm':form1,'error':form.errors})
        else:
            return  render(request,'AdmonCuentas/signup.html',{'sgForm':form,'prForm':form1,'error':"Por favor Ingrese correo institucional de la PUJ"})
    else:
        form = UserCreationForm()
        form1=ProfileForm()
    return render(request,'AdmonCuentas/signup.html',{'sgForm':form,'prForm':form1})

'''
    Funcion que verifica que el correo ingresado por el usuario sea de un dominio especifico,
    en este caso de la javeriana
    
    Parametros
    ----------
    form: UserCreationForm
        formulario que lleva consigo el correo que se quiere revisar.
    
    Retorno
    ----------
    False:
        En caso de que el correo no pertenezca a este dominio.
    True:
        En el caso contrario.
    
'''
def verificar_Correo(form):
    perfil =form.save(commit=False)
    correo= perfil.correo
    partes= correo.split('@')
    if partes[1] != 'javeriana.edu.co':
        return False
    else:
        return True
    

def login_v(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            if 'next' in request.POST:
                return redirect (request.POST.get('next'))
            return redirect('Viajes:Viajes_home')#('appname:linkname')
        else:
            return render(request,'AdmonCuentas/login.html',{'lgForm':form,'error':form.errors})
    else:
        form = AuthenticationForm()
    return render(request,'AdmonCuentas/login.html',{'lgForm':form})
@login_required(login_url="/AdmonCuentas/login/")      
def logout_v(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
        
@login_required(login_url="/AdmonCuentas/login/")
def cambiarRol(request):
    if request.method == 'POST':
        a=User.objects.get(username=request.user.username)
        b= UsuarioTopSeat.objects.get(usuario = a)
        if b.rol ==2:
           b.rol=1
           r='Viajes:pasajero'
        else:
           b.rol=2
           r='Viajes:conductor'
        b.save()
        return redirect("Viajes:Viajes_home")
@login_required(login_url="/AdmonCuentas/login/")
def actualizarContrasena(request):
    datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,data=request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            return redirect('Viajes:Viajes_home')
    else:
        form = PasswordChangeForm(request.user)
        datos['cgForm']=form
    return render(request, 'AdmonCuentas/cambiarContrasena.html',datos)

@login_required(login_url="/AdmonCuentas/login/")
def actualizarPerfil(request):
    datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
    if request.method == 'POST':
        form = editarUsuario(data=request.POST)
        if form.is_valid():
            user= User.objects.get(username=request.user.username)
            datos =form.save(commit =False)
            if datos.first_name != "":
                user.first_name = datos.first_name
            if datos.last_name != "":
                user.last_name = datos.last_name
            user.save()
            return redirect('Viajes:Viajes_home')
    else:
        form = editarUsuario()
        datos['cgForm']=form
    return render(request, 'AdmonCuentas/editarPerfil.html',datos)

def eliminarPerfil(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        user.delete()
        return redirect('home')

@login_required(login_url="/AdmonCuentas/login/")  
def ReporteViajes(request):
    datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request),'Cond':Viaje.objects.filter(conductor__usuario =request.user),'Pasa':Reserva.objects.filter(pasajero__usuario = request.user)}
    return render(request,'AdmonCuentas/reporte.html',datos)


def getRol(request):
    a=User.objects.get(username=request.user.username)
    b= UsuarioTopSeat.objects.get(usuario = a)
    if b.rol == 2:
        rol="Conductor"
    else:
        rol="Pasajero"
    return rol

