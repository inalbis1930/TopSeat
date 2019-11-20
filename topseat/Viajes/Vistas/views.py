# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from .forms import *
from ..Modelo.models import *
from django_google_maps import widgets as map_widgets
from AdmonCuentas.Modelo.models import UsuarioTopSeat
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.views import View
from topseat.ServicioCorreo import servicioCorreo
import json
from django.core.serializers.json import DjangoJSONEncoder


'''
    En este archivo se definen todas las vistas relacionadas a los viajes del sistema
    
    Funciones dispatch para cuando el usuario no esta registrado o autenticado en el sistema.
'''

@method_decorator(login_required, name='dispatch')
class Viajes_homeView(View):
    def post(self, request, *args, **kwargs):
        '''
           En caso de ser un metodo POST significa que el cliente requiere ver el mapa de un viaje, el cual es obtenido por 
            medio de su llave primaria <id>. Envia la informacion necesaria al mapa.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request),'movil':esMovil(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        
        v= Viaje.objects.get(pk=request.POST.get('id','')) #Obtiene el id desde la template
        datos['inicio']=v.ruta.inicio
        datos['fin']=v.ruta.fin
        r = Reserva.objects.filter(viaje=v)
        paradas=[]
        for re in r:
            if re.parada != None:
                paradas.append(re.parada)
        datos['paradas']=json.dumps(list(paradas),cls=DjangoJSONEncoder)
        return render(request,'Viajes/verMapa.html',datos)

    def get(self, request, *args, **kwargs):
        '''
            *En caso de ser un metodo GET puede tener dos resultados, uno que sea pasajero y por lo tanto se le muestran los viajes
            a los cuales se puede registrar y los viajes a los cuales se encuentra registrado como pasajero.
            *En caso de ser conductor se muestran los viajes que tiene activos en este momento y a los pasajeros que tienen
            reservas activas en alguno de sus viajes.
            *En caso de ser iun conductor con un viaje activo entonces se muestra el mapa con las paradas necesarias y la lista
            de sus pasajeros.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request),'movil':esMovil(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        if getRol(request) == "Conductor":
            viaje = Viaje.objects.filter(conductor__usuario =request.user,enCurso=True)
            if viaje.count() ==0: #Si no tiene ningun viaje en curso
                v=Viaje.objects.filter(conductor__usuario =request.user,terminado=False)
                datos['viajes']=v
                r= Reserva.objects.filter(viaje__conductor__usuario=request.user,estado=True)
                datos['reservas']=r
                if 'mensaje' in request.session and request.session['mensaje'] != None:
                    datos['mensaje']=request.session['mensaje']
                    request.session['mensaje']= None
                
                return render(request,'Viajes/conductor.html',datos)
            else:
                return redirect('Viajes:ViajeEnCurso')
        else:
            v=Viaje.objects.filter(puestos_d__gte=1,terminado=False,enCurso=False).exclude(conductor__usuario=request.user)
            datos['viajes']=v
            r= Reserva.objects.filter(pasajero__usuario = request.user,estado=True)
            datos['reservas']=r
            if 'mensaje' in request.session and request.session['mensaje'] != None:
                datos['mensaje']=request.session['mensaje']
                request.session['mensaje']= None
            return render (request,'Viajes/pasajero.html',datos)
    def dispatch(self, request,*args, **kwargs): 
        return super(Viajes_homeView, self).dispatch(request,*args, **kwargs)

def esMovil(request):
    '''
        Funcion que retorna True si el navegador movil y falso en caso contrario.
    '''
    return request.user_agent.is_mobile

    

def getRol(request):
    '''
        Funcion para ser reutilizada para obtener el rol del usuario
    '''
    a=User.objects.get(username=request.user.username)
    b= UsuarioTopSeat.objects.get(usuario = a)
    if b.rol == 2:
        rol="Conductor"
    else:
        rol="Pasajero"
    return rol

@method_decorator(login_required, name='dispatch')
class crearViaje(View):
    def post(self, request, *args, **kwargs):
        '''
            Se hacen las verificaciones necesarias, principalmente que las horas del viaje sean en el futuro y que
            se elija un Vehiculo valido para el viaje
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        form = form_crearViaje(request.user,data=request.POST)
        formruta=form_CrearRuta(data=request.POST)
        datos['nvForm']=form
        datos['rtForm']=formruta
        if form.is_valid():
            viaje=form.save(commit =False)
            if viaje.vehiculo == None:
                datos['error']="Por Favor eliga un Vehiculo"
            else:
                now=datetime.datetime.now()
                if viaje.fecha >  now.date() or (viaje.fecha == now.date() and viaje.hora >= now.time()): #Validacion de fecha y hora
                    ruta=formruta.save()
                    viaje.ruta=ruta
                    viaje.conductor=UsuarioTopSeat.objects.get(usuario=request.user)
                    viaje.save()
                    request.session['mensaje']='Viaje Creado'
                    
                    subject = 'VIAJE CREADO'
                    message = 'Hola \n El viaje del dia: '+ str(viaje.fecha) +" a las " + str(viaje.hora) +' Fue Creado.'
                    recipient_list = [viaje.conductor.correo,]
                    servicioCorreo.enviarCorreo(subject,message,recipient_list)
                    return redirect('Viajes:Viajes_home')
                else: 
                    datos['error']="Por favor ingrese una fecha y hora en el futuro"
                    return render(request,'Viajes/nuevoViaje.html',datos)
        else:
            datos['error']=form.errors
            return render(request,'Viajes/nuevoViaje.html',datos)

    def get(self, request, *args, **kwargs):
        '''
            Se crean los formularios para crear un viaje nuevo y se mandan al Template correspondiente.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)} 
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        v= Vehiculo.objects.filter(dueno=request.user)
        if len(v) ==0:
            return redirect('AdmonCuentas:registro_vehiculo')
        form = form_crearViaje(request.user)
        formruta=form_CrearRuta()
        datos['nvForm']=form
        datos['rtForm']=formruta
        return render(request,'Viajes/nuevoViaje.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(crearViaje, self).dispatch(request,*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class verMapa(View):
    '''
        Clase que se encarga de Mostrar el mapa con sus respectivas paradas al cliente, tanto como conductor como pasajero
    '''
    def post(self, request, *args, **kwargs):
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        v=Vehiculo.objects.filter(dueno=request.user)
        if len(v):
            datos['vehiculos']=v
        return render(request,'Viajes/verMapa.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(verMapa, self).dispatch(request,*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class eliminarViaje(View):
    '''
        Clase que se encarga de identificar un viaje especifico, eliminarlo y avisar a los interesados.
    '''
    def post(self, request, *args, **kwargs):
        viaje =Viaje.objects.get(id=request.POST.get('id',''))
        rs = Reserva.objects.filter(viaje = viaje)
        subject = 'VIAJE ACTUALIZADO'
        message = 'Hola \n El viaje del dia: '+ str(r.viaje.fecha) +" a las " + str(r.viaje.hora) +' Fue Eliminado'
        recipient_list = [viaje.conductor.correo,]
        for r in rs:
            recipient_list.append(r.pasajero.correo)
        servicioCorreo.enviarCorreo(subject,message,recipient_list)
        
        viaje.delete()
        request.session['mensaje']='Viaje Eliminado'
        return redirect('Viajes:Viajes_home')
    def dispatch(self, request,*args, **kwargs):
        return super(eliminarViaje, self).dispatch(request,*args, **kwargs)



@method_decorator(login_required, name='dispatch')
class editarViaje(View):
    def post(self, request, *args, **kwargs):
        '''
            Funcion que verifica cuales fueron los campos que fueron actualizados y los guarda dentro del sistema, revisando
            que sean validos.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        form = modificarViaje(data=request.POST)
        formruta=modificarRuta(data=request.POST)
        if form.is_valid():
            viaje=Viaje.objects.get(pk=request.POST.get('id',''))
            datos= form.save(commit =False)
            datosruta=formruta.save(commit =False)
            ruta=viaje.ruta
            if datosruta.inicio !="":
                ruta.inicio=datosruta.inicio
            if datosruta.fin !="":
                ruta.fin=datosruta.fin
            if datos.puestos_d != None:
                viaje.puestos_d=datos.puestos_d
            if datos.fecha != None:
                viaje.fecha=datos.fecha
            if datos.hora != None:
                viaje.hora=datos.hora
            if datos.vehiculo != None:
                viaje.vehiculo=datos.vehiculo
            if datos.tarifa != None:
                viaje.tarifa=datos.tarifa
            ruta.save()
            viaje.save()
            request.session['mensaje']='Viaje Actualizado'
            
            rs = Reserva.objects.filter(viaje = viaje)
            subject = 'VIAJE ACTUALIZADO'
            message = 'Hola \n El viaje del dia: '+ str(r.viaje.fecha) +" a las " + str(r.viaje.hora) +' Fue modificado, Ingresa a la plataforma para verificar los cambios.'
            recipient_list = [viaje.conductor.correo,]
            for r in rs:
                recipient_list.append(r.pasajero.correo)
            servicioCorreo.enviarCorreo(subject,message,recipient_list)
            
            return redirect('Viajes:Viajes_home')
        else:
            datos['error']=form.errors
            return render(request,'Viajes/nuevoViaje.html',datos)
    def get(self, request, *args, **kwargs):
        '''
            Metodo que crea los formularios correspondientes para modificar la informacion existente dentro de la base de datos sobre
            un viaje en especifico y los envia a la plantilla.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        form = modificarViaje()
        formruta=modificarRuta()
        datos['nvForm']=form
        datos['rtForm']=formruta
        datos['id'] = request.GET.get('id','')
        return render(request,'Viajes/editarViaje.html',datos)
    def dispatch(self, request,*args, **kwargs):
        return super(editarViaje, self).dispatch(request,*args, **kwargs)  



@method_decorator(login_required, name='dispatch')
class confirmarReserva(View):
    def post(self, request, *args, **kwargs):
        '''
            Esta funcion recolecta la informacion sobre la nueva reserva y revisa que sea valida, principalmente la cantidad
            de puestos que quiere reservar, una vez valida crea la reserva y notifica por medio de correo electronico a los
            interesados.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        viaje=Viaje.objects.get(pk=request.POST.get('id',''))
        datos['inicio']=viaje.ruta.inicio
        datos['fin']=viaje.ruta.fin
        datos['viaje']=viaje
        form = f_confirmarReserva(data=request.POST) 
        datos['crForm']=form
        if form.is_valid():
            data= form.save(commit=False)
            cant=int(data.cantidadPuestos)
            if cant< 1 or cant > viaje.puestos_d:
                datos['error']="Por favor ingrese una cantidad de puestos Valida"
                return render(request,'Viajes/confirmarReserva.html',datos)
            else:
                r= Reserva()
                r.pasajero = UsuarioTopSeat.objects.get(usuario=request.user)
                r.viaje=viaje
                r.cantidadPuestos = cant
                if data.parada != None:
                    r.parada = data.parada
                viaje.puestos_d -= cant
                r.save()
                viaje.save()
                request.session['mensaje']='Reserva Realizada'
                
                subject = 'RESERVA EN TOPSEAT[PASAJERO]'
                message = "Hola \n Reservaste "+ str(r.cantidadPuestos)+ " puestos en el viaje del dia: "+ str(r.viaje.fecha) +" a las " + str(r.viaje.hora) +" \nComunicate con tu Conductor "+ viaje.conductor.usuario.first_name+" "+viaje.conductor.usuario.last_name+" al : " +str(viaje.conductor.celular)
                recipient_list = [r.pasajero.correo,]
                servicioCorreo.enviarCorreo(subject,message,recipient_list)
                
                subject = 'RESERVA EN TOPSEAT [CONDUCTOR]'
                message = 'Hola \n El Pasajero '+ str(r.pasajero.usuario.first_name) +" "+str(r.pasajero.usuario.last_name)+ "\n Ha reservado "+ str(r.cantidadPuestos)+ " puestos en tu viaje del dia: "+ str(r.viaje.fecha) +" a las " + str(r.viaje.hora) +" \nComunicate con tu pasajero al : " +str(r.pasajero.celular)
                recipient_list = [viaje.conductor.correo,]
                servicioCorreo.enviarCorreo(subject,message,recipient_list)
                
                return redirect('Viajes:Viajes_home')
        else:
            datos['error']=form.errors
            return render(request,'Viajes/confirmarReserva.html',datos)
    def get(self, request, *args, **kwargs):
        '''
            Esta funcion recolecta toda la informacion correspondiente a un viaje que puede ser candidato para
            la creacion de una reserva, crea los formularios y los envia a la plantilla.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        v=Viaje.objects.get(pk=request.GET.get('id',''))
        r=Reserva.objects.filter(viaje=v,pasajero__usuario=request.user)
        
        if Reserva.objects.filter(viaje=v,pasajero__usuario=request.user).count() ==0:
            datos['inicio']=v.ruta.inicio
            datos['fin']=v.ruta.fin
            form = f_confirmarReserva()
            datos['crForm']=form
            datos['viaje']=v
           
            rs = Reserva.objects.filter(viaje=v)
            paradas=[]
            for re in rs:
                if re.parada != None:
                    paradas.append(re.parada)
            datos['paradas']=json.dumps(list(paradas),cls=DjangoJSONEncoder)
            return render(request,'Viajes/confirmarReserva.html',datos)
        else: 
            request.session['mensaje']='Usted ya tiene una Reserva en este viaje'
            return redirect('Viajes:Viajes_home')
    def dispatch(self, request,*args, **kwargs):
        return super(confirmarReserva, self).dispatch(request,*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class eliminarReserva(View):
    '''
        Clase encargada de obtener una reserva por medio de su Llave Primaria, eliminarla y avisarle a sus interesados.
    '''
    def post(self, request, *args, **kwargs):
        r = Reserva.objects.get(pk=request.POST.get('id',''))
        cant = r.cantidadPuestos
        v= Viaje.objects.get(pk=r.viaje.id)
        v.puestos_d +=cant
        v.save()
        r.delete()
        request.session['mensaje']='Reserva Eliminada'
        
        subject = 'RESERVA ELIMINADA EN TOPSEAT'
        message = 'Hola \n La reserva del Pasajero '+ str(r.pasajero.usuario.first_name) +" "+str(r.pasajero.usuario.last_name)+ "\n ha sido eliminada, por: "+ str(r.cantidadPuestos)+ " puestos en el viaje del dia: "+ str(r.viaje.fecha) +" a las " + str(r.viaje.hora)
        recipient_list = [v.conductor.correo,r.pasajero.correo,]
        servicioCorreo.enviarCorreo(subject,message,recipient_list)
        
        return redirect('Viajes:Viajes_home')
    def dispatch(self, request,*args, **kwargs):
        return super(eliminarReserva, self).dispatch(request,*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class IniciarViaje(View):
    def post(self, request, *args, **kwargs):
        '''
            Funcion que obtiene el viaje por medio de su llave primaria y cambia su estado a enCurso.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        v= Viaje.objects.get(pk=request.POST.get('id',''))
        v.enCurso= True
        v.save()
        return redirect('Viajes:Viajes_home')

    def dispatch(self, request,*args, **kwargs):
        return super(IniciarViaje, self).dispatch(request,*args, **kwargs)

    def get(self, request, *args, **kwargs):
        '''
            Esta funcion recolecta toda la informacion sobre un viaje, con sus respectivas reservas y las envia a la plantilla
            para informar al cliente justo antes de iniciar el viaje.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        v= Viaje.objects.get(pk=request.GET.get('id',''))
        datos['viaje']= v
        datos['inicio']=v.ruta.inicio
        datos['fin']=v.ruta.fin
        r = Reserva.objects.filter(viaje=v)
        datos['reservas']=r
        paradas=[]
        for re in r:
            if re.parada != None:
                paradas.append(re.parada)
        datos['paradas']=json.dumps(list(paradas),cls=DjangoJSONEncoder)
        
        return render(request,'Viajes/IniciarViaje.html',datos)

@method_decorator(login_required, name='dispatch')
class ViajeEnCurso(View):
    def post(self, request, *args, **kwargs):
        '''
            Cuando el viaje haya culminado es necesario desactivar todas las reservas relacionadas con este viaje
            y ponerlo como terminado.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        v= Viaje.objects.get(conductor__usuario=request.user,enCurso=True)
        v.enCurso=False
        v.terminado=True
        v.save()
        r = Reserva.objects.filter(viaje=v)
        for res in r:
            res.estado=False
            res.save()
        request.session['mensaje']='Viaje Terminado con Exito'
        return redirect('Viajes:Viajes_home')
        #Terminar Viaje

    def dispatch(self, request,*args, **kwargs):
        return super(ViajeEnCurso, self).dispatch(request,*args, **kwargs)

    def get(self, request, *args, **kwargs):
        '''
            Esta funcion recolecta toda la informacion sobre un viaje, con sus respectivas reservas y las envia a la plantilla
            para informar al cliente durante el viaje.
        '''
        datos={'usuario':request.user.first_name +" "+request.user.last_name,'rol':getRol(request)}
        img = UsuarioTopSeat.objects.get(usuario=request.user).fotoPerfil
        if img != None:
            datos['img']=img
        v= Viaje.objects.get(conductor__usuario=request.user,enCurso=True)
        datos['viaje']=v
        datos['inicio']=v.ruta.inicio
        datos['fin']=v.ruta.fin
        r = Reserva.objects.filter(viaje=v)
        datos['reservas']=r
        
        paradas=[]
        for re in r:
            if re.parada != None:
                paradas.append(re.parada)
        datos['paradas']=json.dumps(list(paradas),cls=DjangoJSONEncoder)
        
        return render(request,'Viajes/ViajeEnCurso.html',datos)
