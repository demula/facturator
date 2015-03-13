#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from string import Template
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders


def enviar_email(conexion_smtp, email_config, factura):
    email_template = Template(open(email_config.plantilla).read())

    email_body = email_template.substitute(
        email=factura.email,
        number=factura.numero,
        client=factura.cliente,
        total=factura.total,
        fecha=factura.fecha)
    # Create the container (outer) email message.
    msg = MIMEMultipart('related')
    msg['Subject'] = email_config.subject
    msg['From'] = email_config.sender
    msg['To'] = factura.email
    # Añadir texto
    msg_text = MIMEText(email_body, 'html', 'utf-8')
    msg.attach(msg_text)
    # Añadir imagen
    msg_img = MIMEImage(open(email_config.logo_img, 'rb').read(), 'jpeg')
    msg_img.add_header('Content-ID', '<tarjetalia_logo>')
    msg_img.add_header('Content-Disposition', 'inline', filename='tarjetalia_logo.jpg')
    msg.attach(msg_img)
    # Añadir pdf al mensaje
    msg_pdf = MIMEBase('application', 'octet-stream')
    pdf_file = os.path.join('facturas', '%s.pdf' % factura.numero)
    msg_pdf.set_payload(open(pdf_file, 'rb').read())
    encoders.encode_base64(msg_pdf)
    msg_pdf.add_header('Content-Disposition', 'attachment', filename="%s" % os.path.basename(pdf_file))
    msg.attach(msg_pdf)

    # Send the email via our own SMTP server.
    conexion_smtp.sendmail(email_config.sender, factura.email, msg.as_string())