import smtplib
import ssl
from email.message import EmailMessage

# Se define los datos del correo de origen, que envia el mensaje
email_sender = 'pruebapython0@gmail.com'
email_password = 'bbbezeogdykfzfqi'


# metodo para enviar un mensaje a un correo receptor
def send_email(email_receiver, subject, body):

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Se agrega SSL (capa de seguridad)
    context = ssl.create_default_context()

    # Logeo seguro en el correo y envio del mensaje
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())