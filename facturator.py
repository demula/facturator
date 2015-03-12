#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from PyPDF2 import PdfFileWriter, PdfFileReader
import re
import os
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders

EMAIL_IMG = 'tarjetalia_logo.jpg'


def enviar_emails(
                pdf_general,
                plantilla_email,
                email_sender,
                email_subject,
                smtp_server,
                smtp_user,
                smtp_pass):
    # Expresiones regulares para sacar la infor del pdf general
    search_fact_number = re.compile(r'CONCEPTO: (\d+)DOMICILIO:')
    search_fact_email = re.compile(r'E-mail:([0-9A-Za-z\_\-\.]+@[0-9A-Za-z\_\-\.]+\.[0-9A-Za-z\_\-\.]+)www.tarjetalia.es')
    search_fact_client = re.compile(r'n.\d+([A-Za-zÑÁÉÍÓÚÇñáéíóúç0-9\ \t\.\,ªº]+)\t*\n*CIF/NIF/NIE:')
    search_fact_total = re.compile(r'Importe TOTAL(\d+.\d*)')
    search_fact_date = re.compile(r'Tarjetas sin fronteras S.L.(\d+/\d+/\d+)Factura')

    email_template = Template(open(plantilla_email).read())
    input = PdfFileReader(file(pdf_general, "rb"))

    out_number = 0

    print "Conectando al servidor de email..."
    s = smtplib.SMTP()
    s.connect(smtp_server, 587)
    s.login(smtp_user, smtp_pass)
    print "Conectado"
    print "Comienza el proceso y envio de facturas:"
    

    

    for page in input.pages:
        page_text = page.extractText()
        print page.getContents()
        out_number = out_number + 1
        try:
            fact_number = search_fact_number.findall(page_text)[0]
        except:
            print "Fallo al intentar obtener numero de factura"
            exit()

        try:
            fact_email = search_fact_email.findall(page_text)[0]
        except:
            print "Fallo al intentar obtener el email"
            exit()

        try:
            fact_client = search_fact_client.findall(page_text)[0]
        except:
            print "Fallo al intentar obtener el nombre del cliente"
            exit()

        try:
            fact_total = search_fact_total.findall(page_text)[0]
        except:
            print "Fallo al intentar obtener el total de la factura"
            exit()

        try:
            fact_date = search_fact_date.findall(page_text)[0]
        except:
            print "Fallo al intentar obtener la fecha de la factura"
            exit()

        print "     Procesando factura n %s" % fact_number
        output = PdfFileWriter()
        output.addPage(page)
        # Write output
        pdf_file = os.path.join('facturas', '%s.pdf' % fact_number)
        outputStream = file(pdf_file, "wb")
        output.write(outputStream)
        outputStream.close()

        # Send email
        print "     Enviando email a %s" % fact_email
        email_body = email_template.substitute(
                email=fact_email,
                number=fact_number,
                client=fact_client,
                total=fact_total,
                fecha=fact_date)
        # Create the container (outer) email message.
        msg = MIMEMultipart('related')
        msg['Subject'] = email_subject
        msg['From'] = email_sender
        msg['To'] = fact_email
        # Añadir texto
        msg_text = MIMEText(email_body, 'html', 'utf-8')
        msg.attach(msg_text)
        # Añadir imagen
        msg_img = MIMEImage(open(EMAIL_IMG, 'rb').read(), 'jpeg')
        msg_img.add_header('Content-ID', '<tarjetalia_logo>')
        msg_img.add_header('Content-Disposition', 'inline', filename='tarjetalia_logo.jpg')
        msg.attach(msg_img)
        # Añadir pdf al mensaje
        msg_pdf = MIMEBase('application', 'octet-stream')
        pdf_file = os.path.join('facturas', '%s.pdf' % fact_number)
        msg_pdf.set_payload(open(pdf_file, 'rb').read())
        encoders.encode_base64(msg_pdf)
        msg_pdf.add_header('Content-Disposition', 'attachment', filename="%s" % os.path.basename(pdf_file))
        msg.attach(msg_pdf)

        # Send the email via our own SMTP server.
        s.sendmail(email_sender, fact_email, msg.as_string())
    print "Email enviado"

    s.quit()
    print "Se han procesado un total de %i facturas" % out_number


if __name__ == '__main__':
    # Config
    pdf_general = 'facturas.pdf'
    plantilla_email = 'mail_factura.html'
    email_sender = 'facturacion@tarjetalia.es'
    email_subject = 'Facturacion enero - TSF'
    smtp_server = 'mail.tarjetalia.es:587'
    smtp_user = 'facturacion@tarjetalia.es'
    smtp_pass = 'neptuno123'

    enviar_emails(
                pdf_general,
                plantilla_email,
                email_sender,
                email_subject,
                smtp_server,
                smtp_user,
                smtp_pass)
