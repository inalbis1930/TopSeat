from __future__ import unicode_literals
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm,PasswordChangeForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout,update_session_auth_hash
from .forms import *
from ..Modelo.models import *
from django.contrib.auth.decorators import login_required
from Viajes.Modelo.models import *
from Viajes.Vistas.views import *
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.http import HttpResponseRedirect
from topseat.ServicioCorreo import servicioCorreo
'''
    Vistas de la aplicacion de AdmonCuentas.
    Esta aplicacion hace el manejo de las AdmonCuentas, tanto creacion, modificacion, eliminacion,
     cerrar sesion e ingresar al sistema.
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

class home_AdmonCuentas(View):
    def post(self, request, *args, **kwargs):
        return render(request,'AdmonCuentas/home.html')
    def get(self, request, *args, **kwargs):
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
class signup_v(View):
    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        form1 = ProfileForm(request.POST,request.FILES)
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
                subject = 'BIENVENIDO A TOPSEAT' 
                message = 'HOLA, '+usuarioAct.first_name +" "+usuarioAct.last_name+'! \n TE DAMOS UNA CALUROSA BIENVENIDA A TOPSEAT, ENTRAS A MOVILIDAD INTEGRAL! '
                recipient_list = [usuarioAct.email,]
                servicioCorreo.enviarCorreo(subject,message,recipient_list)
                if perfil.rol == 1:
                    return redirect('Viajes:Viajes_home')
                else:
                    return redirect('AdmonCuentas:registro_vehiculo')
            else:
                return  render(request,'AdmonCuentas/signup.html',{'sgForm':form,'prForm':form1,'error':form.errors})
        else:
            return  render(request,'AdmonCuentas/signup.html',{'sgForm':form,'prForm':form1,'error':"Por favor Ingrese correo institucional de la PUJ"})
    def get(self, request, *args, **kwargs):
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
    

class login_v(View):
    def post(self, request, *args, **kwargs):
        '''
            Recolecta la informacion del formulario y verifica que coincida con un usuario que exista dentro de la aplicacion
            en caso de no ser asi devuelve la informacion a la plantilla y muestra un mensaje de error.
            Si toda la informacion es correcta se autentica el usuario dentro de la plataforma
        '''
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            a=User.objects.get(username=request.user.username)
            b= UsuarioTopSeat.objects.get(usuario = a)
            if b.rol==3:
                return redirect('Eventos:Ahome')
            if 'next' in request.POST:
                return redirect (request.POST.get('next'))
            return redirect('Viajes:Viajes_home') #('appname:linkname')
        else:
            return render(request,'AdmonCuentas/login.html',{'lgForm':form,'error':form.errors})
    def get(self, request, *args, **kwargs):
        '''
            Crea el formulario para autenticarse en el sistema y lo envia a la plantilla
        '''
        form = AuthenticationForm()
        return render(request,'AdmonCuentas/login.html',{'lgForm':form})

@method_decorator(login_required, name='dispatch')    
class logout_v(View):
    '''
       Clase que se encarga de cerrar sesion para el usuario que se encuentre autenticado dentro del sistema 
    '''
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
    def dispatch(self, request,*args, **kwargs):
        return super(logout_v, self).dispatch(request,*args, **kwargs)


@method_decorator(login_required, name='dispatch') 
class cambiarRol(View):
    '''
        Clase que se encarga de cambiar de Rol del cliente, de pasajero a conductor y viceversa
    '''
    def post(self, request, *args, **kwargs):
        a=User.objects.get(username=request.user.username)
        b= UsuarioTopSeat.objects.get(usuario = a)
        if b.rol ==2:
           b.rol=1
           r='Viajes:pasajero'
        else:
           b.rol=2
           r='Viajes:conductor'
        b.save()
        return redirect('Viajes:Viajes_home')
    def dispatch(self, request,*args, **kwargs):
        return super(cambiarRol, self).dispatch(request,*args, **kwargs)


@method_decorator(login_required, name='dispatch') 
class actualizarContrasena(View):

    def post(self, request, *args, **kwargs):
        '''
            Recolecta la informacion del formulario y verifica que tanto la contraseña vieja coincida con la que esta guardada
            con la que esta en la base de datos, como que las dos nuevas ingresadas coincidan y sean buenas contraseñas. Envia 
            un correo al usuario quien realiza la modificacion.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        
        form = PasswordChangeForm(request.user,data=request.POST)
        if form.is_valid(): #Valida todos los campos
            user=form.save()
            update_session_auth_hash(request, user)
            subject = 'CAMBIO DE CONTRASEÑ TOPSEAT' 
            message = 'HOLA, '+user.first_name +" "+user.last_name+'! \n Tu contraseña en TOPSEAT fue modificada'
            recipient_list = [user.email,]
            servicioCorreo.enviarCorreo(subject,message,recipient_list)
            return redirect('Viajes:Viajes_home')
    def get(self, request, *args, **kwargs):
        '''
            Crea el formulario para crear una nueva contraseña y lo envia a la plantilla correspondiente
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        form = PasswordChangeForm(request.user)
        datos['cgForm']=form
        return render(request, 'AdmonCuentas/cambiarContrasena.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(actualizarContrasena, self).dispatch(request,*args, **kwargs)

@method_decorator(login_required, name='dispatch') 
class actualizarPerfil(View):
    
    def post(self, request, *args, **kwargs):
        '''
            Recolecta la informacion del formulario y verifica cuales campos fueron modificados y los actualiza dentro de 
            la base de datos. Envia un correo al usuario quien realiza la modificacion.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        form = editarUsuario(request.POST,request.FILES)
        if form.is_valid():
            user= UsuarioTopSeat.objects.get(usuario=request.user)
            datos =form.save(commit =False)
            if request.POST.get('first_name','') != "":
                user.usuario.first_name = request.POST.get('first_name','')
            if request.POST.get('last_name','') != "":
                user.usuario.last_name = request.POST.get('last_name','')
            if datos.celular != "":
                user.celular =datos.celular
            if datos.fotoPerfil != None:
                user.fotoPerfil = datos.fotoPerfil
            user.usuario.save()
            user.save()
            '''subject = 'PERFIL ACTUALIZADO TOPSEAT' 
            message = 'HOLA, '+user.usuario.first_name +" "+user.usuario.last_name+'! \n Tu perfil en TOPSEAT fue modificado'
            recipient_list = [user.email,]
            servicioCorreo.enviarCorreo(subject,message,recipient_list)'''
        return redirect('Viajes:Viajes_home')
    def get(self, request, *args, **kwargs):
        '''
            Crea el formulario para modificar el usuario y lo envia a la plantilla correspondiente.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        form = editarUsuario()
        datos['cgForm']=form
        return render(request, 'AdmonCuentas/editarPerfil.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(actualizarPerfil, self).dispatch(request,*args, **kwargs)

class eliminarPerfil(View):
    '''
        Obtiene un perfil por medio de su llave primaria y lo elimina. Envia un correo al usuario quien realiza la eliminacion.
    '''
    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        
        subject = 'PERFIL ACTUALIZADO TOPSEAT' 
        message = 'HOLA, '+user.first_name +" "+user.last_name+'! \n Tu perfil en TOPSEAT fue Eliminado.\n Lamentamos mucho verte ir, esperamos que vuelvas pronto'
        recipient_list = [user.email,]
        servicioCorreo.enviarCorreo(subject,message,recipient_list) 
        
        user.delete()
        return redirect('home')
        
class eliminarFotoPerfil(View):
    def post(self, request, *args, **kwargs):
        user = UsuarioTopSeat.objects.get(usuario=request.user)
        user.fotoPerfil.delete(save=True)
        return redirect('Viajes:Viajes_home')

@method_decorator(login_required, name='dispatch')
class registrov(View):
    def post(self, request, *args, **kwargs):
        '''
            Recolecta la informacion del vehiculo nuevo, la valida y lo crea asociandolo al usuario quien lo creo.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        form = registrarVehiculo_f(request.POST)
        if form.is_valid():
            a=User.objects.get(username=request.user.username)
            vehiculo = form.save(commit = False)
            vehiculo.dueno = a
            vehiculo.save()
            request.session['mensaje']='Vehiculo Registrado'
            return redirect('Viajes:Viajes_home')#('appname:linkname')

    def get(self, request, *args, **kwargs):
        '''
            Crea el formulario para crear un nuevo vehiculo y lo envia a la plantilla
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        v= Vehiculo.objects.filter(dueno=request.user)
        if len(v) ==0:
            datos['error']="Por favor registre un vehiculo primero"
        form = registrarVehiculo_f()
        datos['rvForm']=form
        return render(request,'AdmonCuentas/registroVehiculo.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(registrov, self).dispatch(request,*args, **kwargs)


@method_decorator(login_required, name='dispatch')  
class ReporteViajes(View):
    '''
        Obtiene todos los viajes de un usuario, tanto de conductor como de pasajero y los envia a la plantilla.
    '''
    def get(self, request, *args, **kwargs):
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request),'Cond':Viaje.objects.filter(conductor__usuario =request.user),'Pasa':Reserva.objects.filter(pasajero__usuario = request.user)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        return render(request,'AdmonCuentas/reporte.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(ReporteViajes, self).dispatch(request,*args, **kwargs)


def getRol(request):
    a=User.objects.get(username=request.user.username)
    b= UsuarioTopSeat.objects.get(usuario = a)
    if b.rol == 2:
        rol="Conductor"
    else:
        rol="Pasajero"
    return rol

@method_decorator(login_required, name='dispatch')
class eliminarVehiculo(View):
    def post(self, request, *args, **kwargs):
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request),'Cond':Viaje.objects.filter(conductor__usuario =request.user),'Pasa':Reserva.objects.filter(pasajero__usuario = request.user)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        f = eliminarV_f(request.user,request.POST)
        if f.is_valid():
            v= Vehiculo.objects.get(pk=request.POST.get('vehiculo',''))
            v.delete()
        return redirect('Viajes:Viajes_home')
    def get(self, request, *args, **kwargs):
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request),'Cond':Viaje.objects.filter(conductor__usuario =request.user),'Pasa':Reserva.objects.filter(pasajero__usuario = request.user)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        cant = Vehiculo.objects.filter(dueno = request.user).count()
        if cant == 0:
            datos['error'] = 'No tienes Vehiculos registrados aún.'
        else:
            f=eliminarV_f(request.user)
            datos['evForm']= f
        return render(request,'AdmonCuentas/eliminarVehiculo.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(eliminarVehiculo, self).dispatch(request,*args, **kwargs)
