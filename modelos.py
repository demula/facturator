#!/usr/bin/env python2
# -*- coding: utf-8 -*-


def extraer_tipo_desde_codigo_factura(codigo_factura):
    return int(codigo_factura.split("-")[0])


def extraer_codigo_desde_codigo_factura(codigo_factura):
    return int(codigo_factura.split("-")[1])


class Factura(object):
    def __init__(self, email, tipo, codigo, nombre_fiscal, total, fecha, numero_cliente, enviada, ruta_archivo_pdf):
        self.email = email
        self.tipo = tipo
        self.codigo = codigo
        self.nombre_fiscal = nombre_fiscal
        self.total = total
        self.fecha = fecha
        self.numero_cliente = numero_cliente
        self.numero = str(self.tipo) + "-" + str(self.codigo)
        self.enviada = enviada
        self.ruta_archivo_pdf = ruta_archivo_pdf

    def esta_enviada(self):
        return self.enviada > 0

    def __str__(self):
        return "Factura(" + "email='" + self.email + "', tipo='" + str(self.tipo) + "', codigo='" + str(
            self.codigo) + "', nombre_fiscal='" + self.nombre_fiscal + "', total='" + str(self.total) + "', fecha='" + str(
            self.fecha) + "', numero_cliente='" + str(self.numero_cliente) + "', numero='" + str(self.numero) + "', enviada='" + str(
            self.enviada) + "', ruta_archivo_pdf='" + str(self.ruta_archivo_pdf) + "')"


class EmailConfig(object):
    def __init__(self, plantilla, logo_img, sender, subject):
        self.plantilla = plantilla
        self.logo_img = logo_img
        self.sender = sender
        self.subject = subject
