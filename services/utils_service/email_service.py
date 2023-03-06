# from threading import Thread
# from . import mail


# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)

# def send_email(to, template, **kwargs):
#     app = current_app._get_current_object()
#     msg = Message("choHoiTot.com",
#                   sender='Team8 Admin <team8@tdtu.com>', recipients=[to])
#     msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr

###Lib smpp###
import smtplib
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from decouple import config

class EmailService():

    def send_mail(self, send_to, title, message, cc=None, files=[]):
        """Compose and send email with provided info and attachments.
        Args:
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        use_tls (bool): use TLS mode
        """
        server="smtp.gmail.com"
        port=587
        use_tls=True
        msg = MIMEMultipart()
        msg['From'] = 'TheSocialHub Team'
        msg['To'] = COMMASPACE.join(send_to)
        if cc:
            msg['Cc'] = COMMASPACE.join(cc)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = title
        username = config('EMAIL_HOST')
        password = config('EMAIL_HOST_PASSWORD')
        

        msg.attach(MIMEText(message))

        for path in files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(op.basename(path)))
            msg.attach(part)

        smtp = smtplib.SMTP(server, port)
        if use_tls:
            smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail('TheSocialHub Team', send_to, msg.as_string())
        smtp.quit()
