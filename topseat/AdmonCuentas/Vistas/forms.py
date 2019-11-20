from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ..roles import *
from ..Modelo.models import *
from ..ClRoles import ROLESNOA


'''
    Formulario para crear un nuevo UsuarioTopSeat. 
'''
class ProfileForm(forms.ModelForm):
    Nombre = forms.CharField(max_length=30,required=True)
    Apellido = forms.CharField(max_length=30,required=True)
    correo = forms.EmailField(max_length=254,required=True, help_text='Por favor introduzca su correo institucional de la P.U Javeriana')
    celular = forms.CharField(max_length=12,required=True)
    rol = forms.ChoiceField(choices= ROLESNOA)
    fotoPerfil = forms.ImageField(required=False, help_text='Opcional')
    class Meta:
        model = UsuarioTopSeat
        fields = ('Nombre','Apellido','correo','celular','rol','fotoPerfil') #Estos son los campos que son mostrados en la plantilla
'''
    Formulario para editar un usuario, ninguno de los campos es obligatorio.
'''
class editarUsuario(forms.ModelForm):
    first_name = forms.CharField(label='Nombre',max_length=30,required=False)
    last_name = forms.CharField(label='Apellido',max_length=30,required=False)
    celular = forms.CharField(max_length=12,required=False)
    fotoPerfil = forms.ImageField(required=False, label='Foto de Perfil')
    class Meta:
        model = UsuarioTopSeat
        fields = ('first_name','last_name','celular','fotoPerfil')


'''
    Formulario para registrar un nuevo vehiculo no necesita el dueño ya que este es extraido de la sesion.
    Todos los campos son obligatorios.
'''
class registrarVehiculo_f(forms.ModelForm):
    modelo = forms.CharField(max_length=50,required= True)
    placa = forms.CharField(max_length=6,required= True)
    color = forms.CharField(max_length=20,required= True)
    class Meta:
        model = Vehiculo
        fields =['modelo','placa','color']
        

class eliminarV_f(forms.Form):
    vehiculo= forms.ModelMultipleChoiceField(queryset=None)
    class Meta:
        fields =['vehiculo']
    def __init__(self, user,*args, **kwargs):
        super(eliminarV_f,self).__init__(*args, **kwargs)
        self.fields['vehiculo'].queryset = Vehiculo.objects.filter(dueno=user) #Query para obtener solo los Vehiculos propios del usuario