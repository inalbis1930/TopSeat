from django.core.mail import send_mail
from django.conf import settings
import _thread


'''
    Clase la cual se encarga del envio de correos electronicos cuando sea necesario.
    Para cada correo que se quiera enviar se recomienda crear un hilo de esta clase que envie
    el correo electronico y de esta manera no interruptir la ejecución normal del programa.
'''
class servicioCorreo:
    """
    Parametros
    ----------
    subject: 
        Asunto que va a quedar registrado para el envio del correo Electronico
    message:
        Mensaje a ser enviado por medio del correo electronico
    recipient_list:
        lista de correos que van a recibir el correo electronico.
    
    """
    def enviarCorreo(subject,message,recipient_list):
        email_from = settings.EMAIL_HOST_USER #Viene desde Settings.py
        _thread.start_new_thread(send_mail,( subject, message, email_from, recipient_list )) 