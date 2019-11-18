from django.core.mail import send_mail
from django.conf import settings
import _thread

class servicioCorreo:
    
    def enviarCorreo(subject,message,recipient_list):
        email_from = settings.EMAIL_HOST_USER
        _thread.start_new_thread(send_mail,( subject, message, email_from, recipient_list ))