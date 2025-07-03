import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class Mail():

    def __init__(self, subject="", text="", recipient=""):

        self.SENDER = "SIMAF Comunica <notificaciones@maximfishing.com>"
        self.RECIPIENT = recipient
        self.AWS_REGION = os.environ['REGION_EMAIL']
        self.ACCESS_KEY = os.environ['KEY_MAIL']
        self.SECRET_ACCESS = os.environ['SECRET_MAIL']
        self.SUBJECT = subject
        self.TEXT = text
        self.ATTACHMENT = r"Path\file\to\send.txt"
        self.BODY_TEXT = text
        self.BODY_HTML = """\
                <html>
                <head></head>
                <body>
                <p>Cordial saludo,</p>
                <p></p>
                <p>""" + self.TEXT + """</p>
                <p></p>
                </body>
                </html>
                """
        self.CHARSET = "utf-8"
        self.msg = MIMEMultipart('mixed')

    def start_aws_session(self):
        """Abrimos la sesion con el SDK"""
        self.client = boto3.client(
            'ses',
            region_name=self.AWS_REGION,
            aws_access_key_id=self.ACCESS_KEY,
            aws_secret_access_key=self.SECRET_ACCESS,
        )
    def build_mail(self):
        """Construimos el objeto del mensaje el cual va a ser enviar por medio del SDK"""
        response = self.client.verify_email_identity(EmailAddress='notificaciones@maximfishing.com')
        print(response['ResponseMetadata']['RequestId'])
        self.msg['Subject'] = self.SUBJECT
        self.msg['From'] = self.SENDER
        #self.msg['To'] = self.RECIPIENT
        #self.msg['X-Odoo-Objects'] = 'account.invoice-108'
        self.msg['X-Odoo-db-uuid'] = response['ResponseMetadata']['RequestId']
        msg_body = MIMEMultipart('alternative')
        textpart = MIMEText(self.BODY_TEXT.encode(self.CHARSET), 'plain', self.CHARSET)
        htmlpart = MIMEText(self.BODY_HTML.encode(self.CHARSET), 'html', self.CHARSET)
        # Add the text and HTML parts to the child container.
        msg_body.attach(textpart)
        msg_body.attach(htmlpart)
        self.msg.attach(msg_body)

    def attach_document(self):
        """Abrimos el documento que deseamos enviar y lo anexamos al objeto Mail"""
        att = MIMEApplication(open(self.ATTACHMENT, 'rb').read())
        att.add_header('Content-Disposition','attachment',filename=os.path.basename(self.ATTACHMENT))
        self.msg.attach(att)

    def send_message(self):
        """
        Enviamos el objeto Mail que construimos en la funcion build_mail y lo enviamos por medio
        del objeto client embebido en el try para captar posibles errores
        """
        try:
            response = self.client.send_raw_email(
                Source=self.SENDER,
                Destinations=self.RECIPIENT,
                RawMessage={
                    'Data': self.msg.as_string(),
                },
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])


def createMail(subject, text, recipient):
    # Inicializamos el objeto
    mail_object = Mail(subject=subject, text=text, recipient=recipient)
    # Iniciamos la sesion con el SDK
    mail_object.start_aws_session()
    # Construimos el correo
    mail_object.build_mail()
    # Adjutamos el archivo que deseamos enviar
    # mail_object.attach_document()
    # Enviamos el mensaje
    mail_object.send_message()