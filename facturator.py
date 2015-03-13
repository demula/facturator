#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join, abspath

import pyodbc
from modelos import EmailConfig
from user_data import extraer_datos_factura_desde_access_db, marcar_factura_enviada_access_db
from send_email import enviar_email


EMAIL_IMG = 'tarjetalia_logo.jpg'
DBfile = 'resources/factusol_database.mdb'


def enviar_emails(carpeta_pdf_facturas,
                  plantilla_email,
                  email_sender,
                  email_subject,
                  smtp_server,
                  smtp_user,
                  smtp_pass):
    out_number = 0

    email_config = EmailConfig(plantilla_email, EMAIL_IMG, email_sender, email_subject)
    archivos_facturas = [(f.split(".")[0], abspath(f)) for f in listdir(carpeta_pdf_facturas) if
                         isfile(join(carpeta_pdf_facturas, f))]

    print "Conectando al servidor de email..."
    s = smtplib.SMTP()
    s.connect(smtp_server, 587)
    s.login(smtp_user, smtp_pass)
    print "Conectado"

    print "Abriendo archivo de base de datos " + DBfile + "..."
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + DBfile)
    cursor = conn.cursor()
    print "Archivo Microsoft Access abierto"

    print "Comienza el proceso y envio de facturas:"
    for (numero_factura, ruta_archivo_pdf) in archivos_facturas:
        print "     Procesando factura n %s" % numero_factura
        try:
            factura = extraer_datos_factura_desde_access_db(cursor, numero_factura, ruta_archivo_pdf)

            # Send email
            print "     Enviando email a %s" % factura.email
            if not factura.esta_enviada():
                enviar_email(s, email_config, factura)
                print "Email enviado"
                marcar_factura_enviada_access_db(conn, cursor, factura)
                print "Factura marcada como enviada"
            else:
                print "Email factura ya previamente enviado"
            out_number = out_number + 1
        except:
            print "     ERROR procesando factura n %s" % numero_factura

    cursor.close()
    conn.close()
    s.quit()
    print "Se han procesado un total de %i facturas" % out_number


if __name__ == '__main__':
    # Config
    carpeta_pdf_facturas = 'facturas'
    plantilla_email = 'mail_factura.html'
    email_sender = 'emai_sender_user@example.com'
    email_subject = 'Email subject'
    smtp_server = 'mail.example.com:587'
    smtp_user = 'emai_sender_user@example.com'
    smtp_pass = '1234'

    enviar_emails(carpeta_pdf_facturas,
                  plantilla_email,
                  email_sender,
                  email_subject,
                  smtp_server,
                  smtp_user,
                  smtp_pass)
